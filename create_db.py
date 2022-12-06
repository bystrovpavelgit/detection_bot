""" Apache License 2.0 Copyright (c) 2020 Pavel Bystrov
    create database """
from webapp.db import DB
from webapp import create_app

DB.create_all(app=create_app())
