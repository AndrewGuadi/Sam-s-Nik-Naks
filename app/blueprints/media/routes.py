from __future__ import annotations

from flask import render_template

from ... import data
from . import media


@media.route("/")
@media.route("/index")
def videos():
    groups = data.get_videos_grouped()
    return render_template("media/videos.html", groups=groups)
