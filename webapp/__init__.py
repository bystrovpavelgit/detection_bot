""" Apache License 2.0 Copyright (c) 2020 Pavel Bystrov
    Flask app """
import os
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_login import LoginManager
from webapp.business_logic import detect, car_count
from webapp.db import DB
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.stat.views import blueprint as stat_blueprint


def create_app():
    """ starting app for Flask object detection site """
    app = Flask(__name__, static_url_path="/webapp/static")
    app.config.from_pyfile("config.py")
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    DB.init_app(app)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(stat_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(user_id)
        return user

    def process_file(request):
        file = request.files["file"]
        if file:
            os.makedirs("webapp/static", exist_ok=True)
            file_name = os.path.join("webapp", "static", file.filename)
            file.save(file_name)
            return file_name

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/cars/", methods=["GET"])
    def count_cars():
        return render_template("submit.html", main_text="Count cars")

    @app.route("/cars/", methods=["POST"])
    def count_cars():
        file_name = process_file(request)
        if file_name is None:
            flash("Ошибка загрузки файла")
            return redirect(url_for("index"))
        answer = car_count(file_name)
        return render_template("show_cars.html", main_img=f"/{answer[1]}", answer=answer[0])

    @app.route("/defects/", methods=["GET"])
    def detect_defects():
        return render_template("submit.html", main_text="Detect defects")

    @app.route("/defects/", methods=["POST"])
    def detect_defects():
        file_name = process_file(request)
        if file_name is None:
            flash("Ошибка загрузки файла")
            return redirect(url_for("index"))
        answer = detect(file_name)
        return render_template("show_result.html", main_img=f"/{file_name}", answer=answer)

    return app
