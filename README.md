- [О проекте](#о-проекте)
- [Архитектура приложения](#архитектура-приложения)
  - [Архитектурная схема компонентов приложения](#архитектурная-схема-компонентов-приложения)
  - [Комментарии](#комментарии)
    - [Модель данных](#модель-данных)
    - [Entities](#entities)
    - [Репозитории](#репозитории)
    - [Прочие компоненты `app.core`](#прочие-компоненты-appcore)
    - [Пользовательские интерфейсы](#пользовательские-интерфейсы)
    - [Фоновые задачи](#фоновые-задачи)
    - [Асинхронность](#асинхронность)
- [CI/CD](#cicd)
- [Live demo](#live-demo)
- [Техническая информация](#техническая-информация)
  - [Запуск в локальном окружении](#запуск-в-локальном-окружении)
  - [Запуск тестов](#запуск-тестов)


# О проекте

Данный микросервис решает следующую задачу: собирать и хранить данные о "свечках" [1] по ценным бумагам, обращающимся на Московской бирже, а также предоставлять доступ другим сервисам системы к этим данным.

[1] [https://ru.wikipedia.org/wiki/Японские_свечи](https://ru.wikipedia.org/wiki/%D0%AF%D0%BF%D0%BE%D0%BD%D1%81%D0%BA%D0%B8%D0%B5_%D1%81%D0%B2%D0%B5%D1%87%D0%B8)

Основной функционал:

- добавление ценных бумаг в базу с помощью команды CLI `create-security`;
- загрузка данных с API Московской биржи в виде фоновой задачи `update_candles` на движке TaskIQ;
- предоставление доступа к данным для потребителей через REST API.

# Архитектура приложения

## Архитектурная схема компонентов приложения

<img src="https://storage.yandexcloud.net/armsmaster/candlestick-service-architecture.drawio.png">

В формате pdf: https://storage.yandexcloud.net/armsmaster/candlestick-service-architecture.drawio.pdf

## Комментарии

### Модель данных

Модель данных описана декларативно в модуле `./db_schema/models.py` с помощью `sqlalchemy.orm`.

Управление миграциями осуществляется с помощью `alembic`.

Сервис `candlestick-service-migrate` в `compose.yaml` отвечает за применение миграций при первом запуске проекта.

### Entities

`app.core.entities` содержит определения сущностей домена: `Security` (ценная бумага), `Candle` (свеча), `CandleSpan` (техническая сущность, которая соответствует периоду, за который свечи ценной бумаги сохранены в хранилище приложения - чтобы исключить избыточные повторные обращения к источнику).

Сущности реализованы как неизменяемые датаклассы.

### Репозитории

Репозитории спроектированы как коллекции сущностей со следующими особенностями:

- содержат методы `add(...)` и `remove(...)`
- поддерживают протокол асинхронной итерации
- содержат метод `count()`
- поддерживают слайсинг в методе `__getitem__(...)`
- содержат методы фильтрации `filter_by_...(...)`
- применение слайсинга и вызов методов фильтрации возвращает копию репозитория, который является коллекцией соответствующего подмножества сущностей

### Прочие компоненты `app.core`

Класс `core.date_time.Timestamp` является утилитным классом, который упрощает работу с датами и временем. По сути является оберткой для `datetime.datetime` и `datetime.date` со вспомогательными методами.

Компонент `IMarketDataAdapter` отвечает за получение торговых данных из внешнего источника (api Московской биржи iss.moex.com).

Компонент `IMarketDataLoader` отвечает за загрузку торговых данных в базу. Для этого он пользуется функционалом маркет дата адаптера и репозиториев. Маркет дата лоадер использует и актуализирует данные `CandleSpan` для гарантии отсутствия дублирующих запросов данных у источника.

### Пользовательские интерфейсы

Приложение содержит два клиентских интерфейса: **CLI-интерфейс** и **REST api**.

Они определены в пакете `app.io` и реализованы с помощью библиотек `typer` и `fastapi` соответственно.

### Фоновые задачи

Фоновые задачи реализованы в пакете `app.tasks` с помощью библиотеки `taskiq`.

### Асинхронность

Все обращения к внешним веб-сервисам реализованы асинхронно с помощью `aiohttp`.

Работа с БД также реализована асинхронно средствами `sqlalchemy.ext.asyncio`.

REST api также использует асинхронные возможности `fastapi`.

Имплементация маркет дата адаптера (`app.market_data_adapter`) реализует асинхронные обращения к внешнему API и обработку результатов с помощью паттерна producer-consumer и функционала `asyncio.Queue`.

Сервис приложения `app.use_cases.update_candles` предназначен для регулярного обновления торговых данных в системе и использует этот же паттерн для асинхронной обработки нескольких ценных бумаг и таймфреймов.

# CI/CD

Автоматизированная сборка и деплой live demo настроены для self-hosted инстанса гитлаба: https://gitlab.armsmaster.ru/r-wand/candlestick-service.

Пайплайны описаны в `.gitlab-ci.yml`.

# Live demo

https://candlestick.armsmaster.ru/docs

# Техническая информация

## Запуск в локальном окружении

Workdir: `.`

```
docker compose up -d -- build
```

## Запуск тестов

```
pytest app
```