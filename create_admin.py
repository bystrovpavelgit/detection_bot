""" Apache License 2.0 Copyright (c) 2020 Pavel Bystrov
    create admin user utility """
from getpass import getpass
import sys
from webapp import create_app
from webapp.db import DB
from webapp.user.models import User

app = create_app()

with app.app_context():
    username = input("Введите имя пользователя: ")

    if User.query.filter(User.username == username).count():
        print("Такой пользователь уже есть")
        sys.exit(0)

    password = getpass("Введите пароль: ")
    password2 = getpass("Повторите пароль: ")
    if not password == password2:
        print("password != password2")
        sys.exit(0)
    new_user = User(username=username, role="admin")
    new_user.set_password(password)

    DB.session.add(new_user)
    DB.session.commit()
    print("User with id {} added".format(new_user.id))
