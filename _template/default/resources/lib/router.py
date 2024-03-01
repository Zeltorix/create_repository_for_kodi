# -*- coding: utf-8 -*-
# Module: router
# Author: Zeltorix
# Created on: 2024.03.01
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
"""
Модуль плагина для KODI 19.x "Matrix" и выше.
Не тестируемый модуль.
"""
# Стандартные модули
from urllib.parse import parse_qsl


# Импорт модуля плагина
from .model import main
from .kodi_api import


# Функция переключения поступающий данных
def router(data_string: str) -> None:
    try:
        # Преобразование поступающей строки в словарь
        # parse_qsl - разбирает строку на параметры и их значения
        params_dict: dict = dict(parse_qsl(data_string))
    except TypeError:
        raise TypeError(f"Нельзя представить как словарь: {data_string}")

    if params_dict:
        if params_dict["router"] == "main":
            _view.output(main())
    else:
        raise ValueError(f"Не нашлось нужных ключей: {params_dict}")
    else:
        _view.output(main())
