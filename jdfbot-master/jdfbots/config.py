# -*- coding: utf-8 -*-
"""Configurations of jdfbots."""

import os

# pylint: disable=invalid-name
cfg = dict()

# Path to database in production setup
cfg["db_path_prod"] = (
    "postgresql://"
    + os.environ.get("POSTGRES_USER", "")
    + ":"
    + os.environ.get("POSTGRES_PASSWORD", "")
    + "@jdfbots-db/"
    + os.environ.get("POSTGRES_DB", "")
)

# Path to database in development setup
cfg["db_path_dev"] = "sqlite:///" + os.path.join(os.getcwd(), "jdf.db")

# Path to logfile in production setup
cfg["logfile_path_prod"] = "/var/jdf/logs/logfile.log"

# Path to logfile in development setup
cfg["logfile_path_dev"] = os.path.join(os.getcwd(), "logfile.log")
