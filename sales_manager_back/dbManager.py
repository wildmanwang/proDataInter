from apps import app, db
from flask_migrate import Migrate

migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(host=app.config["WEB_SERVER_HOST"], port=app.config["WEB_SERVER_PORT"], debug=True)
