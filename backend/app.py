import os
import logging
from flask import Flask
from config import Config
from extensions import db

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    app.logger.setLevel(logging.INFO)

    db.init_app(app)

    with app.app_context():
        import models
        db.create_all()
        from seed import run_seed
        run_seed()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug = True, port = 8443)