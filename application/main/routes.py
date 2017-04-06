from application.main.app import app
from application.models.models import User, Bucketlists, Items, db


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    app.run()
