import logging
from flask import Flask
from config import Config
from extensions import db, migrate, jwt, mail
from routes import register_blueprints
from seed import run_seed

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    app.logger.setLevel(logging.INFO)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    register_blueprints(app)

    with app.app_context():
        db.create_all()
        print("[APP]\tAll DB Tables Created.")
        run_seed()
        print("[SEED]\tDB Seeding Complete.")


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug = True, port = 8443)