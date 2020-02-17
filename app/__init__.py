from flask import Flask
import os
from app.models import db


app = Flask(__name__)

app.config.from_object("app.config.DebugConfig")
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

db.init_app(app)

from app.views import *
