from application.main.app import app
from application.models.models import User, db


@app.route('/')
def hello_world():
    new_user = User("brian", "brian@ret.com", "password")
    print("here")
    add_to_db(new_user)
    return 'Hello, World!'


def add_to_db(model_obj):
    db.session.add(model_obj)
    db.session.commit()

if __name__ == "__main__":
    app.run()
