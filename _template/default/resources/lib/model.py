# -*- coding: utf-8 -*-
# Module: model
# Author: Zeltorix
# Created on: 2024.03.01
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
"""
Модуль плагина для KODI 19.x "Matrix" и выше.
Модуль создания модели данных для интерфейса KODI.
"""

from .data import data


def main() -> dict:
    model: list = []

    for item in data:
        model.append({
            "title": item,
            "icon": item,
            "router": "main"
        })

    return {
        "category": "Standard KODI icons",
        "list": tuple(model)
    }
