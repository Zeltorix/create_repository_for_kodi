# -*- coding: utf-8 -*-
# Module: create_repository
# Author: Zeltorix
# Created on: 2024.03.01
# License: ShawarmaWare(BeerWare)

from json import loads, dumps
import shutil
import os
import zipfile
import tempfile
from pathlib import Path
from xml.etree.ElementTree import XMLParser, TreeBuilder, parse, Element, ElementTree
from time import perf_counter
from hashlib import md5

try:
    from git import Repo  # pip install GitPython
except ImportError:
    raise RuntimeError("Требуется установить GitPython: pip install gitpython")


class CreateRepo:
    """
    Создание репозитории адонов KODI

    :param str branch: Подкаталог общий для исходников и репозитории, по умолчанию "my_repo"
    :param str repository_dir: Каталог куда будет собираться репозитория, по умолчанию "repository"
    :param str source_dir: Каталог откуда будет собираться репозитория, по умолчанию "source"
    :param str base_addons_time_dir: Каталог базы адонов, по умолчанию "base_plugin", только для локального отслеживания
    :param str base_addons_time_file: Файл база, по умолчанию "base.json", только для локального отслеживания
    :param bool base_addons_local: Включение локального отслеживания, по умолчанию False
    :param Path target_dir: Начальный путь с которого скрипт начинает свою работу, по умолчанию текущий каталог,
                            нужен также для работы GIT, должна указана корнева папка GIT репозитории
    """

    __slots__ = [
        "__target_dir",
        "__branch",
        "__source_dir",
        "__repo_dir",
        "__base_addons_time_dir",
        "__base_addons_time_file_path",
        "__base_addons_local",
    ]

    def __init__(self,
                 branch: str = "my_repo",
                 *,
                 repository_dir: str = "repository",
                 source_dir: str = "source",
                 base_addons_time_dir: str = "base_plugin",
                 base_addons_time_file: str = "base.json",
                 base_addons_local: bool = False,
                 target_dir=Path().cwd()) -> None:

        # Папка ветки
        self.__target_dir = target_dir
        # Папка ветки
        self.__branch = branch
        # Папка с исходниками ветки
        self.__source_dir = Path(target_dir, source_dir, branch)
        # Папка репозитории ветки
        self.__repo_dir = Path(target_dir, repository_dir, branch)
        # Папка база для сохранения времени изменения плагинов
        self.__base_addons_time_dir = Path(target_dir, base_addons_time_dir)
        # База для сохранения времени изменения плагинов
        self.__base_addons_time_file_path = Path(target_dir, base_addons_time_dir, base_addons_time_file)
        # Включает локальную базу
        self.__base_addons_local = base_addons_local

        # Очистка базы времени изменения плагинов от несуществующих
        # self._clear_trash_in_data_time()

        # Проверка существований попок и файла базы
        self.__check_dir()

    def __check_dir(self):
        if not Path(self.__source_dir).exists():
            Path(self.__source_dir).mkdir(parents=True, exist_ok=True)
        if not Path(self.__repo_dir).exists():
            Path(self.__repo_dir).mkdir(parents=True, exist_ok=True)
        if self.__base_addons_local:
            if not Path(self.__base_addons_time_dir).exists():
                Path(self.__base_addons_time_dir).mkdir(parents=True, exist_ok=True)
            if not Path(self.__base_addons_time_file_path).is_file():
                with open(Path(self.__base_addons_time_file_path), "w") as fail:
                    fail.write(dumps({}, indent=2))

    def __set_version_addon(self, name_addon: str) -> bool:
        # оставляет комментарии
        parser = XMLParser(target=TreeBuilder(insert_comments=True))
        # Открывает файл, где записана версия плагина
        addon_meta = Path(self.__source_dir, name_addon, "addon.xml")
        with open(addon_meta, "r", encoding="utf-8") as file:
            tree = parse(file, parser=parser)
        root = tree.getroot()
        # Получение версии плагина
        ver: str = root.get("version")
        addon_id = root.get("id")
        ver_major, ver_minor, ver_patch = ver.split(".")
        ver_build_major = ""
        ver_build_minor = ""
        ver_build_patch = ""

        def __build(symbol: str):
            if len(ver.split(symbol)) == 2:
                ver_build = ver.split(symbol)[-1]
                if len(ver_build.split(".")) == 3:
                    ver_build_major, ver_build_minor, ver_build_patch = ver_build.split(".")
                    if ver_build_patch.isdigit():
                        ver_build_patch = int(ver_build_patch) + 1
                elif len(ver_build.split(".")) == 2:
                    ver_build_major, ver_build_minor = ver_build.split(".")
                    if ver_build_minor.isdigit():
                        ver_build_minor = int(ver_build_minor) + 1
                elif ver_build.isdigit():
                    if len(ver_build) == 3:
                        ver_build = str(int(ver_build) + 1).zfill(3)
                    else:
                        ver_build = int(ver_build) + 1

        # Повышение версий сборок
        if "+" in ver:
            __build("+")
        # Повышение предварительной версии сборок
        elif "~" in ver:
            __build("~")

        ver_new = f"{ver_major}.{ver_minor}.{int(ver_patch) + 1}"
        if ver_build_major:
            if "+" in ver:
                ver_new = ver_new + f"+{ver_build_major}"
            elif "~" in ver:
                ver_new = ver_new + f"~{ver_build_major}"

            if ver_build_minor:
                ver_new = ver_new + f".{ver_build_minor}"
                if ver_build_patch:
                    ver_new = ver_new + f".{ver_build_patch}"
        root.set("version", ver_new)
        # Сохранение файла с новой версией
        tree.write(addon_meta, encoding="utf-8", xml_declaration=True)
        print(f"Версия \033[32m{addon_id}\033[0m повышена с \033[31m{ver}\033[0m до \033[31m{ver_new}\033[0m")
        return True

    def __check_addon(self, name_addon: str) -> bool:
        if self.__base_addons_local:
            pass
        else:
            if Repo(self.__target_dir).is_dirty(path=Path(self.__source_dir, name_addon)):
                if self.__set_version_addon(name_addon):
                    return True

    def __zip_create(self, path_addon: Path):
        # Открывает файл, метаданных
        addon_meta = Path(path_addon, "addon.xml")
        with open(addon_meta, "r", encoding="utf-8") as file:
            tree = parse(file, parser=XMLParser(target=TreeBuilder(insert_comments=True)))
        root = tree.getroot()
        addon_version: str = root.get("version")
        addon_id: str = root.get("id")

        if not Path(self.__repo_dir, addon_id).is_dir():
            Path(self.__repo_dir, addon_id).mkdir(parents=True)

        archive_path = Path(
                    self.__repo_dir,
                    addon_id,
                    f"{addon_id}-{addon_version}.zip"
                )
        with zipfile.ZipFile(
                file=archive_path,
                mode="w",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=9,  # 0-9
        ) as archive:
            for item in path_addon.rglob("*"):
                archive.write(item, item.relative_to(path_addon))

        self.___add_checksum_fail(archive_path)

    @staticmethod
    def ___add_checksum_fail(path_file: Path):
        with open(path_file, 'rb') as file_zip:
            hash_fail = md5(file_zip.read()).hexdigest()
        with open(f"{path_file}.md5", "w", encoding="utf-8") as file_hash:
            file_hash.write(hash_fail)

    def __update_metadata_addon(self, path_addon: Path):
        list_copy_files = ["addon.xml"]
        addon_meta = Path(path_addon, "addon.xml")

        # Открывает файл, метаданных
        with open(addon_meta, "r", encoding="utf-8") as file:
            tree = parse(file, parser=XMLParser(target=TreeBuilder(insert_comments=True)))

        addon_id = tree.getroot().get("id")

        for tag in tree.iter():
            if tag.tag in ["icon", "fanart", "banner", "clearlogo", "screenshot"]:
                list_copy_files.append(tag.text)

        for fail in list_copy_files:
            target_path = Path(path_addon, fail)
            new_path = Path(self.__repo_dir, addon_id, fail)
            if target_path.is_file():
                try:
                    shutil.copy(target_path, new_path)  # Для Python 3.8+.
                except:
                    shutil.copy(str(target_path), str(new_path))  # Для Python <= 3.7.

    def __reload_metadata_for_repository(self):
        root = Element('addons')
        for addon in Path(self.__repo_dir).iterdir():
            if addon.is_dir():
                with open(Path(self.__repo_dir, addon, "addon.xml"), "r", encoding="utf-8") as file_addon:
                    tree = parse(file_addon, parser=XMLParser(target=TreeBuilder(insert_comments=True)))
                root.append(tree.getroot())
                tree = ElementTree(root)
                metadata_repository = Path(self.__repo_dir, "addons.xml")
                with open(metadata_repository, 'w', encoding="utf-8"):
                    tree.write(metadata_repository, encoding='UTF-8', xml_declaration=True)
                self.___add_checksum_fail(metadata_repository)

    def create(self):
        print(f"Начат сбор репозитории \033[33m{self.__branch}\033[0m")
        time_start = perf_counter()
        get_update = False
        for addon in self.__source_dir.iterdir():
            if addon.is_dir() and self.__check_addon(addon.name):
                get_update = True
                garbage_collection(addon)
                self.__zip_create(addon)
                self.__update_metadata_addon(addon)

        if get_update:
            self.__reload_metadata_for_repository()
        else:
            print(f"Изменений в репозитории \033[33m{self.__branch}\033[0m нет")
        print(f"Затрачено на \033[33m{self.__branch}\033[0m \033[35m{perf_counter() - time_start:0.3f}\033[0m секунд(ы)")


def garbage_collection(target_dir: Path = Path.cwd()):

    def delete_junk(f):
        try:
            shutil.rmtree(f)
        except:
            Path(f).unlink()

    def clean_all_from_junk(directory):
        for item in Path(directory).iterdir():
            if item.name == "__pycache__":
                print("Удалено --> ", item)
                delete_junk(item)
            else:
                if Path(item).is_dir():
                    clean_all_from_junk(item)

    try:
        walk = Path(target_dir).walk()
    except AttributeError:
        walk = os.walk(target_dir)

    for path, dirs, files in walk:
        clean_all_from_junk(path)
