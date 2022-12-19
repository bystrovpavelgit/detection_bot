""" Apache License 2.0 Copyright (c) 2020 Pavel Bystrov
    configuration """
import logging
import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(filename='webapp.log', level=logging.INFO)

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "webapp.db")
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "WERFTYUhj342678gvmjhxckbdvkjbsdvk"
REMEMBER_COOKIE_DURATION = timedelta(days=5)
ENCODER_FILE = "model/label_encoder.pkl"
CLSF_MODEL = "model/mobilenetv2_80_3_cl.dict"
COUNT_CARS = "Count cars"
