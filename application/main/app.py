from flask import Flask

app = Flask(__name__)

# SQLALCHEMY_TRACK_MODIFICATIONS might cause a lot of overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False