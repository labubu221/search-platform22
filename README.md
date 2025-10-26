# 🚀 People Search Platform

Универсальная платформа для поиска людей с машинным обучением, AI-поиском и интеллектуальными рекомендациями.

## ⚡ Быстрый старт (один шаг!)

```bash
cd /home/sigmar/Downloads/people-search-platform22
./clean-and-start.sh
```

Затем откройте: **http://localhost**

Войдите с тестовым аккаунтом:
- **Email**: john.doe@example.com
- **Password**: password123

## 📚 Документация

**🇷🇺 ПОЛНАЯ ДОКУМЕНТАЦИЯ НА РУССКОМ:**

Откройте файл **`ПОЛНОЕ_РУКОВОДСТВО.txt`** - он содержит:
- Подробные инструкции по запуску
- Описание всех функций
- Информацию о backend и frontend
- Список всех 10 тестовых аккаунтов
- Пошаговое тестирование
- Решение всех проблем
- Команды управления

## ✨ Ключевые возможности

- ✅ **ML-рекомендации** - интеллектуальный подбор по совместимости
- ✅ **AI-поиск** - поиск на естественном языке
- ✅ **Детальные профили** - интересы, навыки, цели
- ✅ **Система match'ей** - like/dislike с взаимными совпадениями
- ✅ **Мессенджер** - личные сообщения
- ✅ **Аналитика** - визуализация данных
- ✅ **Мультиязычность** - English, Русский, Deutsch
- ✅ **Автосоздание** - 10 тестовых пользователей при запуске

## 🛠️ Технологии

**Backend:**
- Python 3.11, FastAPI, SQLAlchemy
- PostgreSQL, Redis
- Scikit-learn (ML)
- JWT аутентификация

**Frontend:**
- React 18, React Router
- Axios, React Context
- Recharts (графики)

**Инфраструктура:**
- Docker, Docker Compose
- Nginx

## 📦 Структура проекта

```
people-search-platform22/
├── backend/                    # FastAPI Backend
│   ├── app/                    # Основной код
│   │   ├── routers/            # API endpoints
│   │   ├── main.py             # FastAPI app
│   │   ├── models.py           # БД модели
│   │   └── ml_engine.py        # ML алгоритм
│   ├── init_db.py              # ⭐ Инициализация БД
│   ├── create_10_test_users.py # ⭐ Создание пользователей
│   └── docker-entrypoint.sh    # ⭐ Docker entrypoint
│
├── frontend/                   # React Frontend
│   └── src/components/         # React компоненты
│
├── docker-compose.yml          # Docker конфигурация
├── clean-and-start.sh          # ⭐ Скрипт запуска
├── simple-start.sh             # Запуск без Docker
└── ПОЛНОЕ_РУКОВОДСТВО.txt      # 🇷🇺 Полная документация
```

## 🎯 Способы запуска

### С Docker (рекомендуется)

Автоматически создаёт 10 тестовых пользователей:

```bash
./clean-and-start.sh
```

### Без Docker

```bash
./simple-start.sh
```

Затем создайте пользователей:
```bash
cd backend
export DATABASE_URL="sqlite:///./people_search.db"
python3 create_10_test_users.py
```

## 👥 Тестовые аккаунты

Пароль для всех: **password123**

1. john.doe@example.com - Software Developer (San Francisco)
2. jane.smith@example.com - UI/UX Designer (New York)
3. mike.wilson@example.com - Fitness Trainer (Los Angeles)
4. sarah.johnson@example.com - Data Scientist (Chicago)
5. alex.brown@example.com - Musician (Seattle)
6. emma.davis@example.com - Marketer (Boston)
7. david.martinez@example.com - Developer/Teacher (Austin)
8. olivia.taylor@example.com - Entrepreneur (Miami)
9. james.anderson@example.com - Photographer (Denver)
10. sophia.lee@example.com - UX Researcher (Portland)

## 🧪 Тестирование

1. **Login** - войдите с любым тестовым аккаунтом
2. **Profile** - просмотр и редактирование профиля
3. **Recommendations** - ML-рекомендации с % совместимости
4. **Discover** - поиск с фильтрами (город, возраст, навыки)
5. **AI Search** - "Find developers in San Francisco"
6. **Like/Dislike** - на профилях других пользователей
7. **Messages** - личные сообщения
8. **Analytics** - визуализация данных
9. **Language** - переключение языка 🇬🇧 🇷🇺 🇩🇪

## 📖 Подробная документация

**Откройте файл `ПОЛНОЕ_РУКОВОДСТВО.txt`** для:
- Детальных инструкций по каждой функции
- Описания архитектуры backend и frontend
- Работы с базой данных
- Решения всех возможных проблем
- Команд управления Docker и приложением

## 🆘 Помощь

**Порт занят?**
```bash
./clean-and-start.sh  # Автоматически освободит порты
```

**Docker не работает?**
```bash
./simple-start.sh  # Запуск без Docker
```

**Подробное решение проблем:**
См. раздел "10. РЕШЕНИЕ ПРОБЛЕМ" в файле `ПОЛНОЕ_РУКОВОДСТВО.txt`

## 📝 Лицензия

Этот проект создан как демонстрация платформы для поиска людей с использованием современных веб-технологий и машинного обучения.

---

**🚀 Приятного использования!**

Для полной информации откройте **`ПОЛНОЕ_РУКОВОДСТВО.txt`**

