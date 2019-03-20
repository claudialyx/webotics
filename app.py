import os
import config
from flask import Flask

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'webotics_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

