# Notes API

Проект реализует **RESTful API** для управления заметками с использованием **FastAPI**. Включает в себя валидацию, структурированную архитектуру, обработку ошибок и комплексное тестирование.

## 📁 Структура проекта

```
notes_api/
├── app/
│   ├── main.py           # Точка входа в приложение
│   ├── schemas.py        # Pydantic-схемы и валидаторы
│   ├── models.py         # Хранилище заметок (или будущие ORM-модели)
│   ├── services.py       # Бизнес-логика для заметок
│   └── routes/
│       └── notes.py      # Маршруты API
├── tests/
│   └── test_api.py       # Pytest-тесты для эндпоинтов и валидации
└── requirements.txt      # Зависимости
```

## 🚀 Возможности

* **CRUD-операции** (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`)
* **HEAD** и **OPTIONS** для проверки ресурсов и метаданных CORS
* **Валидация Pydantic** с ограничениями полей и проверкой дат
* **Глобальные обработчики исключений** для единообразных ответов об ошибках
* **CORS middleware** включён
* **Логирование** неожиданных ошибок
* **Документация OpenAPI** доступна по адресам `/docs` и `/redoc`

## ⚙️ Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/yourusername/notes_api.git
   cd notes_api
   ```

2. Создайте виртуальное окружение и установите зависимости:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .\.venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

## ▶️ Запуск приложения

1. Активируйте виртуальное окружение, если оно ещё не активно:

   ```bash
   source .venv/bin/activate   # Linux/macOS
   .\.venv\Scripts\activate  # Windows
   ```

2. Перейдите в корневую папку проекта (ту, где находится `app/`):

   ```bash
   cd path/to/notes_api
   ```

3. Запустите сервер разработки с автоматической перезагрузкой:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   * **--host** `0.0.0.0` позволяет принимать запросы извне (например, в Docker).
   * **--port** можно заменить на другой, если порт 8000 занят.
   * **--reload** автоматически перезапускает сервер при изменениях в коде.

4. Откройте в браузере:

   * Основное API: `http://localhost:8000`
   * Swagger UI: `http://localhost:8000/docs`
   * ReDoc: `http://localhost:8000/redoc`

## 📑 Эндпоинты API

| Метод   | Путь          | Описание                               |
| ------- | ------------- | -------------------------------------- |
| GET     | `/notes/`     | Получить список всех заметок           |
| GET     | `/notes/{id}` | Получить заметку по ID                 |
| POST    | `/notes/`     | Создать новую заметку                  |
| PUT     | `/notes/{id}` | Полностью обновить заметку             |
| PATCH   | `/notes/{id}` | Частично обновить заметку              |
| DELETE  | `/notes/{id}` | Удалить заметку                        |
| HEAD    | `/notes/{id}` | Проверить наличие (без тела ответа)    |
| OPTIONS | `/notes/`     | Получить список поддерживаемых методов |

### Модели запросов и ответов

* **`NoteCreate`**: `title` (от 1 до 100 символов), необязательное `content` (до 1000 символов), необязательное будущее `due_date`.
* **`NoteUpdate`**: те же поля, все опциональны.
* **`NoteOut`**: включает `id`, проверенные поля и `due_date`.

## 🧪 Тестирование

Запустите тесты командой:

```bash
pytest
```

Тесты проверяют:

* Успешные CRUD-сценарии
* 404 при отсутствии ресурса
* Ошибки валидации (например, прошедшая `due_date`)
