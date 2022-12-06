""" configuration """
import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "webapp.db")
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "WERFTYUhj342678gvmjhxckbdvkjbsdvk"
REMEMBER_COOKIE_DURATION = timedelta(days=5)
