from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../models/yolos.db'
# SQLALCHEMY_TRACK_MODIFICATIONS might cause a lot of overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False