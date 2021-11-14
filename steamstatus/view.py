from flask import Blueprint, jsonify, render_template

from steamstatus.data import REGIONS
from steamstatus.service import get_latest_status

bp = Blueprint("view", __name__)


@bp.route("/")
def index():
    return render_template("index.html.jinja", regions=REGIONS)


@bp.route("/status")
def status():
    return jsonify(get_latest_status().data)
