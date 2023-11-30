from flask import Flask
from app.auth.apis import auth_blueprint
from app.user.apis import user_blueprint
from app.job.apis import job_blueprint
from infrastructure.db import db

import os

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)

app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(job_blueprint, url_prefix="/job")


@app.route("/", methods=["GET"])
def health_check():
    return "OK", 200
