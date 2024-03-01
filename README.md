# Автоматический сборщик репозиторий для адонов KODI
### Требуется Python 3.6 и выше, желательно 3.12 (для pathlib.Path().walk())

### Требуется установить строение пакеты/модули:

- GitPython
```
pip install GitPython
```
### Требуется создать GIT репозиторию

#### Возможности сборщика:
- Создает структуру отдельный путь для исходников, отдельный путь для репозитория
- Автоматически повышает версию адона, а именно персию патча 0.0.x, посредством GIT или локальной базы(дорабатывается)
- Не удаляет комментарии при работе с файлами ".xml"
- Автоматически удаляет мусор типа папок \__pycache\__ перед сборкой
- Архивирует в zip файл и создает файл хеш суммы
- Копирует все картинки описанные в файле адона addon.xml, согласно их путям
- Создаёт репозиторию KODI и её структуру, addons.xml, файл хеш суммы, отдельные папки под адоны
- Не копируются лишние файлы, которые не участвующие в выдачи информации, типа лицензии, но не в самом архиве, только в репозитории

#### Возможные баги при использовании GIT в качестве отслеживания изменения в файлах
- Версия повышается при каждом запуске скрипта сборщика
- - Решение:
- - - Версия повышается относительно последнего комита в папки с адоном
- - - Требуется сделать комит для этих изменений, тогда не будет повышаться версия

#### Примеры использования описаны в файлах run*.py

#### Примеры кодов адонов в процессе, времени пока нет.
Для примера будут написаны плагины аудио и видео, также плагины показывающие возможности интерфейса.