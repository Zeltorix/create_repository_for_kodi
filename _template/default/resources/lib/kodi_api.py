# -*- coding: utf-8 -*-
# Module: view
# Author: Zeltorix
# Created on: 2024.03.01
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
"""
Плагин для KODI 19.x "Matrix" и выше.
"""
# Стандартные модули
import sys
from urllib.parse import urlencode
from pathlib import Path

# Модули KODI
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs


class DialogProgress:
    __slots__ = ["dialog"]

    def __init__(self):
        self.dialog = xbmcgui.DialogProgress()

    def create(self, header: str, message: str):
        return self.dialog.create(header, message)

    def is_canceled(self) -> bool:
        return self.dialog.iscanceled()

    def update(self, percent: int(0 - 100), message: str):
        return self.dialog.update(percent, message)

    def close(self):
        return self.dialog.close()


# Получите URL-адрес плагина в формате plugin://id_плагина.
url = sys.argv[0]
# ID плагина
id_plugin: str = url.split("/")[2]
# Получить заготовка плагина в виде целого числа.
handle: int = int(sys.argv[1])
kodi_version_major: int = int(xbmc.getInfoLabel("System.BuildVersion").split(".")[0])


def convert_to_url(**kwargs) -> str:
    # Преобразование ключа и значения в ссылку данных для дополнения в виде URL
    return f"{url}/?{urlencode(kwargs)}"


def jsonrpc(data: str) -> str:
    return xbmc.executeJSONRPC(data)


def script(data: str):
    return xbmc.executescript(data)


def reload(**kwargs) -> None:
    xbmc.executebuiltin(f"Container.Update({convert_to_url(**kwargs)})")


def get_plugin_info(api_key: str, addon_id: str = None):
    # author, changelog, description, disclaimer, fanart, icon, id, name, path, profile, stars, summary, type,
    # version
    if addon_id:
        return xbmcaddon.Addon(addon_id).getAddonInfo(api_key)
    return xbmcaddon.Addon().getAddonInfo(api_key)


def get_windows_width_height() -> dict:
    get_height = xbmcgui.Window().getHeight()
    get_width = xbmcgui.Window().getWidth()
    if get_width > get_height:
        height = get_height
        width = get_width
    else:
        width = get_height
        height = get_width
    return {
        "width": width,
        "height": height,
    }


def open_settings(addon_id: str = None):
    if addon_id:
        return xbmcaddon.Addon(addon_id).openSettings()
    return xbmcaddon.Addon().openSettings()


def get_setting_str(api_key: str, addon_id: str = None) -> str:
    if addon_id:
        return xbmcaddon.Addon(addon_id).getSetting(api_key)
    return xbmcaddon.Addon().getSetting(api_key)


def get_setting_bool(api_key: str, addon_id: str = None) -> bool:
    if addon_id:
        return xbmcaddon.Addon(addon_id).getSettingBool(api_key)
    return xbmcaddon.Addon().getSettingBool(api_key)


def get_setting_int(api_key: str, addon_id: str = None) -> int:
    if addon_id:
        return xbmcaddon.Addon(addon_id).getSettingInt(api_key)
    return xbmcaddon.Addon().getSettingInt(api_key)


def set_setting(id_: str, value: str, addon_id: str = None) -> bool:
    if addon_id:
        xbmcaddon.Addon(addon_id).setSetting(id=id_, value=value)
    xbmcaddon.Addon().setSetting(id=id_, value=value)
    return True


def dialog_text_input(label: str = "Ввод текста") -> str:
    item = xbmcgui.Dialog().input(
        label,
        type=xbmcgui.INPUT_ALPHANUM)

    return item


def dialog_input(type_: str = "text", label: str = "Ввод", autoclose: int = None) -> str:
    type_input = xbmcgui.INPUT_ALPHANUM
    if type_ == "text":
        type_input = xbmcgui.INPUT_ALPHANUM
    elif type_ == "int":
        type_input = xbmcgui.INPUT_NUMERIC
    elif type_ == "date":
        label += " (format: DD/MM/YYYY)"
        type_input = xbmcgui.INPUT_DATE
    elif type_ == "time":
        label += " (format: HH:MM)",
        type_input = xbmcgui.INPUT_TIME
    elif type_ == "ip":
        label += " (format: #.#.#.#)"
        type_input = xbmcgui.INPUT_IPADDRESS

    if autoclose:
        return xbmcgui.Dialog().input(
            heading=label,
            type=type_input,
            autoclose=autoclose,
        )

    return xbmcgui.Dialog().input(
        heading=label,
        type=type_input,
    )


def dialog_notification(heading: str, message: str, type_message: str = "info") -> None:
    if type_message == "warning":
        notification = xbmcgui.NOTIFICATION_WARNING
    elif type_message == "error":
        notification = xbmcgui.NOTIFICATION_ERROR
    elif type_message == "info":
        notification = xbmcgui.NOTIFICATION_INFO
    else:
        notification = xbmcgui.NOTIFICATION_INFO

    xbmcgui.Dialog().notification(
        heading=heading,
        message=message,
        icon=notification,
        time=5000,
    )


def dialog_ok(heading: str, message: str) -> bool:
    return xbmcgui.Dialog().ok(heading=heading, message=message)


def dialog_yesno(heading: str, message: str) -> bool:
    return xbmcgui.Dialog().yesno(heading=heading, message=message)


def dialog_select(header: str, data: list) -> int:
    return xbmcgui.Dialog().select(header, data, useDetails=True)


def dialog_text_viewer(heading: str, message: str, monospace_font: bool = False) -> bool:
    return xbmcgui.Dialog().textviewer(heading=heading, text=message, usemono=monospace_font)


def check_modules() -> None:
    def target_module(check_module: str) -> None:
        try:
            xbmcaddon.Addon(check_module)
        except:
            xbmcgui.Dialog().notification(
                heading=f"Установка библиотеки {check_module}",
                message=f"{check_module}",
                icon=xbmcgui.NOTIFICATION_WARNING,
                time=5000)
            xbmc.executebuiltin(f"RunPlugin('plugin://{check_module}')")

    target_module("inputstream.adaptive")


def restart():
    xbmc.restart()


def logs(
        message: str,
        level: (xbmc.LOGDEBUG,
                xbmc.LOGINFO,
                xbmc.LOGWARNING,
                xbmc.LOGERROR,
                xbmc.LOGFATAL,
                int) = xbmc.LOGERROR
        ) -> None:
    """
    Вывод лога в журнал KODI.

    :param str message:  Сообщение для вывода в логи.
    :param int level:    Тип вывода логов, по умолчанию тип ОШИБКИ

    ===============  ===============  =========================
    Значение тестом  Значение числом  Описание
    ===============  ===============  =========================
    LOGDEBUG         0                Для дебагера
    LOGINFO          1                Для информационных
    LOGNOTICE        2                Для вывода оповещений
    LOGWARNING       3                Для вывода предупреждений
    LOGERROR         4                Для вывода ошибок
    LOGFATAL         5                Для вывода
    ===============  ===============  =========================
    Используются либо текстовые значение либо числовые
    """
    if level == xbmc.LOGERROR or level == 4 or level == xbmc.LOGFATAL or level == 5:
        xbmc.log(
            msg=f"{id_plugin}\n\n\n{message}\n\n",
            level=level
        )
    elif get_setting_bool("log"):
        xbmc.log(
            msg=f"{id_plugin}\n\n\n{message}\n\n",
            level=level
        )


def play(data: (str, dict), manifest_type: (str, bool) = False) -> None:
    if type(data) is dict:
        path = data["link_play"]
        manifest_type = data["type"]
        if data.get("add_headers"):
            for header, value in data["add_headers"].items():
                headers[header] = value
    else:
        path = data

    if manifest_type == "mdp":
        mime_type = "application/dash+xml"
    else:
        mime_type = "application/x-mpegURL"

    # Создаю элемент с указанием url для воспроизведения.
    play_item = xbmcgui.ListItem(path=path)

    if get_setting_bool("inputstream", "script.module.zeltorix.utilitys"):
        if get_setting_bool("inputstream_adaptive_bool", "script.module.zeltorix.utilitys") and manifest_type:
            # Использовать inputstream.adaptive для входящего медиапотока
            play_item.setProperty("inputstream", "inputstream.adaptive")

            if kodi_version_major < 21:
                # Тип манифеста медиапотока
                play_item.setProperty("inputstream.adaptive.manifest_type", manifest_type)
                # Обновление манифеста, возможно это убирает баг с зависанием
                play_item.setProperty("inputstream.adaptive.manifest_update_parameter", "full")

            if get_setting_bool("inputstream_adaptive_selection_resolution_bool",
                                     "script.module.zeltorix.utilitys"):
                selection_resolution = [
                    "adaptive",
                    "fixed-res",
                    "ask-quality",
                    "manual-osd",
                ][get_setting_int("inputstream_adaptive_selection_resolution",
                                       "script.module.zeltorix.utilitys")]

                if kodi_version_major == 21 and \
                        get_plugin_info("version", "inputstream.adaptive") < "21.4.1~" and \
                        selection_resolution == "manual-osd":
                    # Выбор разрешения перед просмотром
                    play_item.setProperty('inputstream.adaptive.stream_selection_type', 'ask-quality')
                else:
                    # Выбор разрешения в меню
                    play_item.setProperty("inputstream.adaptive.stream_selection_type", selection_resolution)

            # Заголовки для загрузки манифестов и потоков (аудио/видео/субтитры) до KODI 20
            play_item.setProperty("inputstream.adaptive.stream_headers", urlencode(headers))

            if kodi_version_major >= 20:
                play_item.setProperty("inputstream.adaptive.manifest_headers", urlencode(headers))

            # Тип запрашиваемого контента
            play_item.setMimeType(mime_type)
            # Если отключено, запросы HEAD, например, для определения типа mime, не будут отправляться.
            play_item.setContentLookup(False)

        elif get_setting_bool("inputstream_ffmpegdirect_bool", "script.module.zeltorix.utilitys"):
            play_item.setProperty("inputstream", "inputstream.ffmpegdirect")

    # Передача элемента в оболочку проигрывателя Kodi.
    xbmcplugin.setResolvedUrl(handle=handle, succeeded=True, listitem=play_item)


def output(input_data: dict) -> None:
    if input_data.get("content"):
        # files, songs, artists, albums, movies, tvshows, episodes, musicvideos, videos, images, games
        xbmcplugin.setContent(handle, input_data["content"])
    else:
        content: str = [
            "files",  # 0
            "songs",  # 1
            "artists",  # 2
            "albums",  # 3
            "movies",  # 4
            "tvshows",  # 5
            "episodes",  # 6
            "musicvideos",  # 7
            "videos",  # 8
            "images",  # 9
            "games"  # 10
        ][int(get_setting_str("view_content", "script.module.zeltorix.utilitys"))]
        xbmcplugin.setContent(handle, content)

    if input_data.get("category"):
        xbmcplugin.setPluginCategory(handle, input_data["category"])
    else:
        xbmcplugin.setPluginCategory(handle, "")

    if input_data.get("sort"):
        for sort in input_data["sort"]:
            xbmcplugin.addSortMethod(handle, sort)
    else:
        xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_NONE)

    for item in input_data["list"]:
        list_item = xbmcgui.ListItem(label=item["title"])

        if item.get("context_menu"):
            list_item.addContextMenuItems(item["context_menu"])

        if kodi_version_major >= 20:
            vinfo = list_item.getVideoInfoTag()
            vinfo.setTitle(item["title"])
            if item.get("plot"):
                vinfo.setPlot(item["plot"])
            if item.get("genres"):
                vinfo.setGenres(item["genres"])
            if item.get("premiered"):
                vinfo.setPremiered(item["premiered"])
            if item.get("duration"):
                vinfo.setDuration(item["duration"])
            if item.get("episode"):
                vinfo.setEpisode(item["episode"])
            if item.get("season"):
                vinfo.setSeason(item["season"])
            if item.get("dateadded"):
                vinfo.setDateAdded(item["dateadded"])
            if item.get("year"):
                vinfo.setYear(item["year"])
            if item.get("votes"):
                vinfo.setVotes(item["votes"])
            vinfo.setMediaType("video")
        else:
            list_item.setInfo("video", {"title": item["title"]})
            if item.get("plot"):
                list_item.setInfo("video", {"plot": item["plot"]})
            if item.get("genres"):
                list_item.setInfo("video", {"genre": item["genres"]})
            if item.get("premiered"):
                list_item.setInfo("video", {"premiered": item["premiered"]})
            if item.get("duration"):
                list_item.setInfo("video", {"duration": item["duration"]})
            if item.get("episode"):
                list_item.setInfo("video", {"episode": item["episode"]})
            if item.get("season"):
                list_item.setInfo("video", {"season": item["season"]})
            if item.get("dateadded"):
                list_item.setInfo("video", {"dateadded": item["dateadded"]})
            if item.get("year"):
                list_item.setInfo("video", {"year": item["year"]})
            if item.get("votes"):
                list_item.setInfo("video", {"votes": item["votes"]})
            list_item.setInfo("video", {"mediatype": "video"})

        if item.get("images"):
            list_item.setArt({"thumb": item["images"]})
            list_item.setArt({"icon": item["images"]})
            list_item.setArt({"fanart": item["images"]})

        if item.get("thumb"):
            list_item.setArt({"thumb": item["thumb"]})
        if item.get("poster"):
            list_item.setArt({"poster": item["poster"]})
        if item.get("banner"):
            list_item.setArt({"banner": item["banner"]})
        if item.get("fanart"):
            list_item.setArt({"fanart": item["fanart"]})
        if item.get("clearart"):
            list_item.setArt({"clearart": item["clearart"]})
        if item.get("clearlogo"):
            list_item.setArt({"clearlogo": item["clearlogo"]})
        if item.get("landscape"):
            list_item.setArt({"landscape": item["landscape"]})
        if item.get("icon"):
            list_item.setArt({"icon": item["icon"]})

        if item.get("select"):
            list_item.select(item["select"])

        # Внутренний переход есть
        is_folder: bool = True
        if item.get("not_folder"):
            is_folder: bool = False
        if item.get("play"):
            list_item.setProperty("IsPlayable", "true")
            # Переход внутрь не требуется, можно отключить
            is_folder: bool = False
        if not item.get("router") and not item.get("data"):
            is_folder: bool = False
        if item.get("router"):
            router = item["router"]
        else:
            router = ""
        url: str = convert_to_url(router=router)
        if item.get("data") and type(item["data"]) is dict:
            url: str = convert_to_url(router=router, **item["data"])
        elif item.get("data"):
            url: str = convert_to_url(router=router, data=item["data"])

        xbmcplugin.addDirectoryItem(handle, url, list_item, is_folder)

    xbmcplugin.endOfDirectory(handle)
