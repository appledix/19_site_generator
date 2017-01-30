# Encyclopedia

В данном репозитории хранится скрипт, собирающий сайт из набора статей энциклопедии образовательного ресурса [DEVMAN.org](https://devman.org).

Папка `/docs` - результат работы скрипта, её содержимое используется для хостинга на GitHub pages. Ознакомиться можно тут - [devman articles](https://appledix.github.io/19_site_generator/docs/index.html).

Статьи хранятся в `/articles`. 
Используемые шаблоны страниц в `/templates`.
Css и javascript файлы, а также иконки хранятся в `/static`.
Местоположение конкретных статей с названиями и разделами указано в файле `config.json`.

### Использование скрипта
В терминале: `python3.5 site_generator.py`

По умолчанию, после создания папки с сайтом (при последующих запусках) скрипт перезаписывает **все** файлы.

В случае необходимости обновления можно передать скрипту флаг "-light".
Пример: `python3.5 site_generator.py -light`
При наличии флага скрипт генерирует и пересобирает только те файлы, последняя модификация которых была раньше последней модификации исходников. 

### Установка скрипта 
В терминале: `git clone https://github.com/appledix/19_site_generator.git`

## Установка зависимостей
В терминале: `pip3 install -r requirements.txt`


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)