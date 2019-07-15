# -*- coding: utf-8 -*-
"""
«J'arrête de Fumer» bots.

This package provides the bots for the «J'arrête de Fumer» program.
"""

import os
import logzero
from flask import Flask, send_from_directory

# Load `.env` file -- EARLY
if not os.environ.get("JDF_PRODUCTION"):
    from dotenv import load_dotenv

    load_dotenv()

from jdfbots import facebook
from jdfbots.config import cfg
from jdfbots.models import DB, MIGRATE

# Define Production/Development configurations
if os.environ.get("JDF_PRODUCTION", ""):
    DB_PATH = cfg["db_path_prod"]
    logzero.logfile(cfg["logfile_path_prod"], maxBytes=10e6, backupCount=5)
else:
    DB_PATH = cfg["db_path_dev"]
    logzero.logfile(cfg["logfile_path_dev"], maxBytes=100e6, backupCount=1)

# Create and configure the Flask app
APP = Flask(__name__)
APP.config["SQLALCHEMY_DATABASE_URI"] = DB_PATH
APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# Ignore trailing slashes!
APP.url_map.strict_slashes = False

# Setup database and migration
DB.init_app(APP)
MIGRATE.init_app(APP)

# Register blueprints
APP.register_blueprint(facebook.BP, url_prefix="/facebook")

# Serve static Files
@APP.route("/static/<filename>")
@APP.route("/static/<path:path>/<filename>")
def send_static(filename, path=""):
    """Send static files."""
    return send_from_directory(os.path.join("../static", path), filename)


# Serve media Files
@APP.route("/media/<filename>")
@APP.route("/media/<path:path>/<filename>")
def send_media(filename, path=""):
    """Send media files."""
    return send_from_directory(os.path.join("../media", path), filename)
