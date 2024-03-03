# -*- coding: utf-8 -*-
# Module: run
# Author: Zeltorix
# Created on: 2024.03.01
# License: ShawarmaWare(BeerWare)
"""
Простейший пример работы со скриптом сборщиком.

При запуске создаст структуру, отдельную папку для исходников, отдельную папку для репозитория.
Также промежуточную папку с одинаковым название в них, указывающие на то, что они связаны.
"""
from _kodi_repo.create_repository import CreateRepo


def main():
    # При желании можно изменять добавив в CreateRepo() нужные параметры,
    # branch можно вызвать без названия, остальные требуют названия.
    # Пример создаваемых путей, при запуске без параметров:
    # исходники - "\source\my_repo\"
    # репозитории - "\repository\my_repo\"
    #
    # :param str branch: Подкаталог общий для исходников и репозитории, по умолчанию "my_repo"
    # :param str repository_dir: Каталог куда будет собираться репозитория, по умолчанию "repository"
    # :param str source_dir: Каталог откуда будет собираться репозитория, по умолчанию "source"
    # :param Path target_dir: Начальный путь с которого скрипт начинает свою работу, по умолчанию текущий каталог.
    #                         Также нужен для работы GIT, должна указана корнева папка GIT репозитории.

    CreateRepo().create()


if __name__ == '__main__':
    main()
