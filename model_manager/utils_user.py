# -*- coding: utf-8 -*-

import uuid
from PyQt5.QtCore import QSettings

ROOT = "model_manager"
KEY_USER = f"{ROOT}/user_uuid"
KEY_FAV  = f"{ROOT}/favorites"


def get_user_uuid():
    settings = QSettings()
    uid = settings.value(KEY_USER, "", type=str)
    if not uid:
        uid = str(uuid.uuid4())
        settings.setValue(KEY_USER, uid)
    return uid


def get_favorites():
    settings = QSettings()
    uid = get_user_uuid()
    return settings.value(f"{KEY_FAV}/{uid}", [], type=list)


def is_favorite(model_path):
    return model_path in get_favorites()


def add_favorite(model_path):
    settings = QSettings()
    uid = get_user_uuid()
    favs = set(get_favorites())
    favs.add(model_path)
    settings.setValue(f"{KEY_FAV}/{uid}", list(favs))


def remove_favorite(model_path):
    settings = QSettings()
    uid = get_user_uuid()
    favs = set(get_favorites())
    favs.discard(model_path)
    settings.setValue(f"{KEY_FAV}/{uid}", list(favs))
