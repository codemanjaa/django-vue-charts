# -*- coding: utf-8 -*-
"""Internationalization of chatbots."""

import os
import json

from functools import partial
from glob import glob

TRANSLATIONS = dict()


def translate(text, args=None, lang=None):
    """Translate a text to given lang, format it with args if any."""
    translated = text
    if lang in TRANSLATIONS:
        translated = TRANSLATIONS[lang].get(translated, translated)
    if args:
        translated = translated.format(**args)
    return translated


def translate_buttons(buttons, lang=None):
    """Translate buttons to given lang."""
    return [
        {"title": translate(b["title"], lang=lang), "payload": b["payload"]}
        for b in buttons
    ]


def translator(user):
    """Return a translator for a given language."""
    return partial(translate, lang=user.language)


def load_translations():
    """Load translations files in memory."""
    dirname = os.path.dirname(__file__)
    filenames = glob(os.path.join(dirname, "*.json"))
    for filename in filenames:
        lang, _ = os.path.splitext(os.path.basename(filename))
        translations = json.load(open(filename, "r"))
        TRANSLATIONS[lang] = translations


load_translations()
