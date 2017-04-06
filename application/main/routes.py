from application.main.app import app
from application.models.models import User, Bucketlists, Items, db


@app.route('/')
def hello_world():
    new_user = User(username="hj", email="hw@3", password="1")
    return 'Hello, World!'


def add_to_db(model_obj):
    db.session.add(model_obj)
    db.session.commit()


if __name__ == "__main__":
    app.run()
