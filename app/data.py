import json
import os
import sqlite3
from pathlib import Path
from typing import Iterable, List, Optional

from flask import current_app, g


SCHEMA_VERSION = 2


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        database_path = current_app.config["DATABASE_PATH"]
        Path(os.path.dirname(database_path)).mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app) -> None:
    app.teardown_appcontext(close_db)
    with app.app_context():
        initialize()


def initialize() -> None:
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            hero_image TEXT
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            made_to_order INTEGER DEFAULT 0,
            limited_drop INTEGER DEFAULT 0,
            seasonal INTEGER DEFAULT 0,
            bundle_eligible INTEGER DEFAULT 0,
            personalization_schema TEXT,
            availability TEXT DEFAULT 'in_stock',
            options TEXT,
            FOREIGN KEY(category_id) REFERENCES category(id)
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS product_image (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            image_url TEXT NOT NULL,
            alt_text TEXT,
            position INTEGER DEFAULT 0,
            FOREIGN KEY(product_id) REFERENCES product(id)
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS review (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT NOT NULL,
            name TEXT NOT NULL,
            piece_ref TEXT
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS city_page (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            intro TEXT,
            directions TEXT,
            hours TEXT
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS video (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            thumbnail_url TEXT,
            video_url TEXT
        )
        """
    )

    version = db.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
    if not version:
        seed(db)
        db.execute(
            "INSERT INTO meta (key, value) VALUES (?, ?)",
            ("schema_version", str(SCHEMA_VERSION)),
        )
        db.commit()
    elif int(version["value"]) != SCHEMA_VERSION:
        reset(db)
        seed(db)
        db.execute(
            "UPDATE meta SET value = ? WHERE key='schema_version'",
            (str(SCHEMA_VERSION),),
        )
        db.commit()


def reset(db: sqlite3.Connection) -> None:
    tables = [
        "video",
        "city_page",
        "review",
        "product_image",
        "product",
        "category",
    ]
    for table in tables:
        db.execute(f"DELETE FROM {table}")
        db.execute("DELETE FROM sqlite_sequence WHERE name = ?", (table,))


def seed(db: sqlite3.Connection) -> None:
    categories = [
        (
            "earrings",
            "Earrings",
            "Macro sparkle, featherlight feel.",
            "https://images.unsplash.com/photo-1542293787938-4d2226a6767f?auto=format&fit=crop&w=1200&q=80",
        ),
        (
            "trays",
            "Trays",
            "Display-worthy trays with resin clarity.",
            "https://images.unsplash.com/photo-1530023367847-a683933f417f?auto=format&fit=crop&w=1200&q=80",
        ),
        (
            "ashtrays",
            "Ashtrays",
            "Built to look good, made to last.",
            "https://images.unsplash.com/photo-1503602642458-232111445657?auto=format&fit=crop&w=1200&q=80",
        ),
        (
            "dominoes",
            "Dominoes",
            "Game night with a resin glow.",
            "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80",
        ),
        (
            "bottle-openers",
            "Bottle Openers",
            "Solid grip with custom inclusions.",
            "https://images.unsplash.com/photo-1527169402691-feff5539e52c?auto=format&fit=crop&w=1200&q=80",
        ),
        (
            "wearables",
            "Wearables",
            "Pins, pendants, and all the ways to carry resin.",
            "https://images.unsplash.com/photo-1518544801976-3e158c89b286?auto=format&fit=crop&w=1200&q=80",
        ),
    ]
    db.executemany(
        "INSERT INTO category (slug, name, description, hero_image) VALUES (?, ?, ?, ?)",
        categories,
    )

    products = [
        (
            "cosmic-mica-earrings",
            "Cosmic Mica Earrings",
            1,
            "Hand-poured earrings with violet mica, gold leaf, and hypoallergenic hooks.",
            68.0,
            0,
            1,
            0,
            1,
            json.dumps({"engrave": True, "colorways": ["Violet", "Emerald", "Sunset"], "inlays": ["Gold leaf", "Pressed florals"]}),
            "in_stock",
            json.dumps({"sizes": ["Standard"], "inlays": ["Gold leaf", "Pressed florals"], "colorways": ["Violet", "Emerald", "Sunset"]}),
        ),
        (
            "riverstone-serving-tray",
            "Riverstone Serving Tray",
            2,
            "24-inch tray with riverstone pattern and walnut handles.",
            180.0,
            1,
            0,
            1,
            0,
            json.dumps({"engrave": True, "colorways": ["Glacier", "Amber"], "inlays": ["River rock", "Copper flake"]}),
            "made_to_order",
            json.dumps({"sizes": ["18 inch", "24 inch"], "inlays": ["River rock", "Copper flake"], "colorways": ["Glacier", "Amber"]}),
        ),
        (
            "ember-ashtray",
            "Ember Ashtray",
            3,
            "Heat-resistant ashtray with copper shimmer and beveled edges.",
            48.0,
            0,
            0,
            0,
            1,
            json.dumps({"engrave": False, "colorways": ["Copper", "Midnight"], "inlays": ["Mica", "Opal fleck"]}),
            "in_stock",
            json.dumps({"sizes": ["Standard"], "colorways": ["Copper", "Midnight"]}),
        ),
        (
            "aurora-domino-set",
            "Aurora Domino Set",
            4,
            "Double-six domino set with aurora gradient and storage box.",
            125.0,
            1,
            0,
            1,
            0,
            json.dumps({"engrave": True, "colorways": ["Aurora", "Midnight"], "inlays": ["Iridescent flakes"]}),
            "made_to_order",
            json.dumps({"sizes": ["Standard"], "colorways": ["Aurora", "Midnight"]}),
        ),
        (
            "flora-bottle-opener",
            "Flora Bottle Opener",
            5,
            "Heavyweight opener with embedded dried florals.",
            32.0,
            0,
            1,
            0,
            0,
            json.dumps({"engrave": True, "colorways": ["Garden", "Meadow"], "inlays": ["Florals", "Leaf"]}),
            "in_stock",
            json.dumps({"sizes": ["Standard"], "colorways": ["Garden", "Meadow"]}),
        ),
        (
            "opal-pendant",
            "Opal Drift Pendant",
            6,
            "Pendant with opal drift and adjustable chain.",
            58.0,
            0,
            0,
            0,
            1,
            json.dumps({"engrave": False, "colorways": ["Opal", "Tide"], "inlays": ["Iridescent"]}),
            "in_stock",
            json.dumps({"sizes": ["Adjustable"], "colorways": ["Opal", "Tide"]}),
        ),
    ]
    db.executemany(
        """
        INSERT INTO product (
            slug, name, category_id, description, price, made_to_order, limited_drop, seasonal, bundle_eligible,
            personalization_schema, availability, options
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        products,
    )

    images = [
        (1, "https://images.unsplash.com/photo-1503341504253-dff4815485f1?auto=format&fit=crop&w=900&q=80", "Cosmic earrings on velvet"),
        (1, "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?auto=format&fit=crop&w=900&q=80", "Earrings close up"),
        (2, "https://images.unsplash.com/photo-1560448205-4d9b7deb70b9?auto=format&fit=crop&w=900&q=80", "Riverstone tray macro"),
        (3, "https://images.unsplash.com/photo-1470337458703-46ad1756a187?auto=format&fit=crop&w=900&q=80", "Ember ashtray with glow"),
        (4, "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=900&q=80", "Aurora domino set on table"),
        (5, "https://images.unsplash.com/photo-1517686469429-8bdb88b9cb0b?auto=format&fit=crop&w=900&q=80", "Bottle opener with florals"),
        (6, "https://images.unsplash.com/photo-1529946825183-536aff452f5d?auto=format&fit=crop&w=900&q=80", "Opal pendant detail"),
    ]
    db.executemany(
        "INSERT INTO product_image (product_id, image_url, alt_text) VALUES (?, ?, ?)",
        images,
    )

    reviews = [
        ("Gorgeous detail. The tray catches light like glass.", "A., Harrisburg", "Riverstone Serving Tray"),
        ("They turned my idea into something I want to keep forever.", "M., Camp Hill", "Custom Pendant"),
        ("Insanely thoughtful. The inclusions are perfect.", "J., Carlisle", "Cosmic Mica Earrings"),
        ("Worth the wait. Packaging was stunning.", "S., Mechanicsburg", "Aurora Domino Set"),
        ("Feels like holding a memory.", "T., Harrisburg", "Custom Ashtray"),
    ]
    db.executemany(
        "INSERT INTO review (quote, name, piece_ref) VALUES (?, ?, ?)",
        reviews,
    )

    city_pages = [
        (
            "harrisburg",
            "Harrisburg Studio",
            "Our HQ for limited drops and pickups.",
            "Located off Third Street Market. Parking available in the lot after 5pm.",
            "Fri-Sun 11am-6pm",
        ),
        (
            "camp-hill",
            "Camp Hill Pop-ups",
            "Weekend pop-ups with make-and-take minis.",
            "Find us at Market on Market. Street parking available.",
            "Select Saturdays 10am-3pm",
        ),
        (
            "mechanicsburg",
            "Mechanicsburg Markets",
            "Seasonal fairs focused on custom commissions.",
            "Hosted at Liberty Commons. Park in the east lot.",
            "First Sundays 12pm-4pm",
        ),
        (
            "carlisle",
            "Carlisle Events",
            "Trunk shows with collaborative artists.",
            "Downtown arts corridor near Pomfret Street.",
            "Monthly, see Instagram",
        ),
    ]
    db.executemany(
        "INSERT INTO city_page (slug, title, intro, directions, hours) VALUES (?, ?, ?, ?, ?)",
        city_pages,
    )

    videos = [
        ("glow-pour", "Glow Pour Setup", "pours", "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=900&q=80", "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"),
        ("demold-moment", "Demold Moment", "demolds", "https://images.unsplash.com/photo-1600508774685-0e7c0f30b7bb?auto=format&fit=crop&w=900&q=80", "https://samplelib.com/lib/preview/mp4/sample-10s.mp4"),
        ("finishing-pass", "Finishing Pass", "finishing", "https://images.unsplash.com/photo-1582719478181-2cf4eac7ef2b?auto=format&fit=crop&w=900&q=80", "https://samplelib.com/lib/preview/mp4/sample-15s.mp4"),
        ("studio-tour", "Studio Tour", "behind-the-scenes", "https://images.unsplash.com/photo-1545239351-1141bd82e8a6?auto=format&fit=crop&w=900&q=80", "https://samplelib.com/lib/preview/mp4/sample-20s.mp4"),
    ]
    db.executemany(
        "INSERT INTO video (slug, title, category, thumbnail_url, video_url) VALUES (?, ?, ?, ?, ?)",
        videos,
    )

    db.commit()


def _query(sql: str, params: Iterable = ()):  # helper
    db = get_db()
    cur = db.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return rows


def get_categories() -> List[sqlite3.Row]:
    return _query("SELECT * FROM category ORDER BY name")


def get_category_by_slug(slug: str) -> Optional[sqlite3.Row]:
    rows = _query("SELECT * FROM category WHERE slug = ?", (slug,))
    return rows[0] if rows else None


def get_products(category_slug: Optional[str] = None, limited: Optional[bool] = None, search_term: Optional[str] = None) -> List[sqlite3.Row]:
    sql = [
        "SELECT p.*, c.slug as category_slug, c.name as category_name FROM product p",
        "JOIN category c ON p.category_id = c.id",
        "WHERE 1=1",
    ]
    params: List = []
    if category_slug and category_slug != "all":
        sql.append("AND c.slug = ?")
        params.append(category_slug)
    if limited is not None:
        sql.append("AND p.limited_drop = ?")
        params.append(1 if limited else 0)
    if search_term:
        sql.append("AND (p.name LIKE ? OR p.description LIKE ?)")
        like = f"%{search_term}%"
        params.extend([like, like])
    sql.append("ORDER BY p.limited_drop DESC, p.seasonal DESC, p.name")
    query = "\n".join(sql)
    return _query(query, params)


def get_product_by_slug(slug: str) -> Optional[sqlite3.Row]:
    rows = _query(
        """
        SELECT p.*, c.slug AS category_slug, c.name AS category_name
        FROM product p
        JOIN category c ON p.category_id = c.id
        WHERE p.slug = ?
        """,
        (slug,),
    )
    return rows[0] if rows else None


def get_product_images(product_id: int) -> List[sqlite3.Row]:
    return _query(
        "SELECT * FROM product_image WHERE product_id = ? ORDER BY position, id",
        (product_id,),
    )


def get_reviews(limit: Optional[int] = None) -> List[sqlite3.Row]:
    sql = "SELECT * FROM review ORDER BY id"
    if limit:
        sql += " LIMIT ?"
        return _query(sql, (limit,))
    return _query(sql)


def get_city_pages() -> List[sqlite3.Row]:
    return _query("SELECT * FROM city_page ORDER BY id")


def get_city_page(slug: str) -> Optional[sqlite3.Row]:
    rows = _query("SELECT * FROM city_page WHERE slug = ?", (slug,))
    return rows[0] if rows else None


def get_videos_grouped() -> dict:
    rows = _query("SELECT * FROM video ORDER BY category, title")
    grouped: dict = {}
    for row in rows:
        grouped.setdefault(row["category"], []).append(row)
    return grouped
