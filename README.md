## Сайт для проведения олимпиад - Время Олимпиад

```
olympiad_time/
│
├── app/
│   ├── __init__.py        # Инициализация приложения
│   ├── forms/             # Файлы форм
│   │   └── student_form.py
│   │
│   ├── models/            # Файлы моделей
│   │   └── student.py
│   │
│   ├── templates/         # HTML-шаблоны
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── student.html
│   │   └── results.html
│   │
│   ├── static/            # Статические файлы (CSS, JS, изображения)
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── js/
│   │   │   └── scripts.js
│   │   └── images/
│   │       └── trophy.png
│   │
│   ├── routes.py          # Файл маршрутов (роуты приложения)
│   ├── config.py          # Конфигурация приложения
│   └── extensions.py      # Инициализация расширений (например, SQLAlchemy)
│
├── instance/              # Секретные данные (например, база данных)
│   └── olympiad_time.db
│
├── requirements.txt       # Зависимости проекта
└── run.py                 # Главный файл для запуска приложения
```




**Дата:** 20.10.2024

**Версия:** 1.0
