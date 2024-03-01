# -*- coding: utf-8 -*-
# Module: run
# Author: Zeltorix
# Created on: 2024.03.01
# License: ShawarmaWare(BeerWare)
"""
Дополнительный пример
"""
from _kodi_repo.create_repository import CreateRepo

list_repo = [
    # Три отдельных репозитории
    ["template_test_1", "repo_template", "source_template"],
    ["template_test_2", "repo_template", "source_template"],
    ["template_test_3", "repo_template", "source_template"],

    # Собрать из трех репозиторий в одну
    ["", "repo_template/template_test_4", "source_template/template_test_1"],
    ["", "repo_template/template_test_4", "source_template/template_test_2"],
    ["", "repo_template/template_test_4", "source_template/template_test_3"],
]


def main():
    # При желании можно изменять добавив в CreateRepo() нужные параметры,
    # branch можно вызвать без названия, остальные требуют названия.
    #
    # :param str branch: Подкаталог общий для исходников и репозитории, по умолчанию "my_repo"
    # :param str repository_dir: Каталог куда будет собираться репозитория, по умолчанию "repository"
    # :param str source_dir: Каталог откуда будет собираться репозитория, по умолчанию "source"
    # :param Path target_dir: Начальный путь с которого скрипт начинает свою работу, по умолчанию текущий каталог,
    #                         нужен также для работы GIT, должна указана корнева папка GIT репозитории

    for item in list_repo:
        CreateRepo(
            branch=item[0],
            repository_dir=item[1],
            source_dir=item[2],
        ).create()


if __name__ == '__main__':
    main()
