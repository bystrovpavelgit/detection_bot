# Detection Telegram Bot (road check and cars localization)

Please create new chat bot and mongo DB instance for this app. 
You have to create settings.py yourself with content like this:
API_KEY = "1410788878:AAHV9"
MONGO_PWD = ""
MONGO_LINK = "mongodb+srv:/"

Web app and Telegram Bot that detects cars and road defects on uploaded images

requires torchvision 
on first run two torch models will be downloaded in the background from pytorch.org
pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

Object-Detection Telegram Bot requires object_detection/settings.py with API KEY for your chat bot
Try to join BothFather chat bot and run /newbot
File settings.py has 
API_KEY = "<You API KEY>"
MONGO_LINK = "<mongodb url>" 

Object-Detection Telegram Bot requires MongoDB instance or Mongo Atlas instance to be created

Object-Detection Web app requires SQLite db and users created before start
python create_db.py
python create_admin.py

To start Object-Detection web app
Run from root folder (It will take about one minute)
set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run (Windows)

export FLASK_APP=webapp && export FLASK_ENV=development && export FLASK_DEBUG=1 && flask run (Unix/Mac)

To start  Object-Detection Telegram Bot
Run from object_detection folder
python bot.py
