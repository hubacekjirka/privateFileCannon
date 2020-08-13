from flask import Flask

app = Flask(__name__)
# Pick configuration based on FLASK_ENV enviromental variable
if app.config["ENV"] == "production":
    app.config.from_object("config.ProdConfig")
else:
    app.config.from_object("config.DevConfig")

from app import views