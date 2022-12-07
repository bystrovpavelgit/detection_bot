""" Apache License 2.0 Copyright (c) 2020 Pavel Bystrov
    blueprint for statistics"""
import os
from flask import render_template, Blueprint
from flask_login import login_required
from object_detection.charts import get_chart
from webapp.business_logic import get_stats

blueprint = Blueprint("stat", __name__, url_prefix="/stat")


@blueprint.route("/show")
@login_required
def show_stat():
    """show_stat endpoint"""
    answers = get_stats()
    text = answers[0]
    chart_img = "/" + get_chart(os.path.join("webapp", "static"), answers[1], answers[2])
    return render_template("stat/show_stat.html", answers=text, chart_img=chart_img)
