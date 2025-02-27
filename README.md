# Flask Wishlist App

Простий додаток для списку бажань на Flask. Ви можете переглядати бажані подарунки та позначати їх як подаровані.

## Функції

- Перегляд, додавання, редагування та видалення елементів списку бажань
- Позначення елементів як подаровані
- Адміністративний інтерфейс для керування елементами
- Адаптивний дизайн
- Інтерфейс українською мовою

## Встановлення

1. Клонуйте репозиторій:
   ```
   git clone https://github.com/yourusername/flask-wishlist.git
   cd flask-wishlist
   ```

2. Створіть віртуальне середовище та активуйте його:
   ```
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

3. Встановіть залежності:
   ```
   pip install -r requirements.txt
   ```

4. Запустіть додаток:
   ```
   python run.py
   ```

5. Відкрийте браузер і перейдіть за адресою `http://127.0.0.1:5000`

## Використання

- Відвідайте `/` для перегляду списку бажань
- Натисніть на елементи, щоб переглянути деталі та подарувати їх
- Відвідайте `/admin` для керування елементами списку бажань

## База даних

Додаток використовує SQLite з Flask-SQLAlchemy. Файл бази даних `wishlist.db` буде створено автоматично при першому запуску додатка.

## Розгортання на Render

Цей додаток можна розгорнути на [Render](https://render.com/) як веб-сервіс.

1. Створіть новий Web Service на Render, вказавши URL вашого GitHub репозиторію
2. Використовуйте наступні налаштування:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn "app:create_app()"` 

Render автоматично визначить це як додаток Python і виконає необхідні кроки для розгортання.

## Структура проєкту

```
flask-wishlist/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       ├── admin/
│       │   ├── add_product.html
│       │   ├── edit_product.html
│       │   └── index.html
│       ├── base.html
│       ├── index.html
│       └── product_detail.html
├── requirements.txt
├── README.md
└── run.py
```