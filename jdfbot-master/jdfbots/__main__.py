#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script for running «J'arrête de Fumer» bots."""

import os

from jdfbots import APP


def main():
    """Entry point for running the bots."""
    # Workaround for the werkzeug reloader removing the current directory from
    # the path. It's nasty, but it works! Inspired by:
    # https://github.com/mitsuhiko/flask/issues/1246
    os.environ['PYTHONPATH'] = os.getcwd()
    # Run the Flask app
    APP.run(host='0.0.0.0', port=8000, debug=True, threaded=True)


if __name__ == "__main__":
    main()
