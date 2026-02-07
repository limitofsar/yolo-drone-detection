# YOLO Drone Detection 🛸

Проект для детекции объектов с дронов с помощью моделей YOLO (Ultralytics).  
Включает **backend API** (FastAPI) и **веб-интерфейс** (Streamlit) для визуализации результатов.

---

## 📁 Структура проекта

Notebooks/ — Jupyter notebooks с экспериментами и тестами YOLO
backend/ — Backend (FastAPI) для инференса модели
frontend/ — Веб-интерфейс (Streamlit) для просмотра результатов
model_weights/ — Предобученные веса YOLO моделей
src/ — Основной код (загрузка модели)
test/ — Примеры видео для тестирования
requirements.txt — Список зависимостей проекта

---

## 🐍 Совместимость

- Python 3.10+  
- Windows / Linux / macOS  

---

## 🚀 Установка и создание виртуального окружения

```bash
# 1. Клонируем репозиторий
git clone git@github.com:limitofsar/yolo-drone-detection.git
cd yolo-drone-detection

# 2. Создаём виртуальное окружение
python -m venv .venv

# 3. Активируем виртуальное окружение
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# 4. Устанавливаем зависимости
pip install -r requirements.txt
```

---
## 🖥 Запуск проекта
1️⃣ Backend (FastAPI)
Запуск из корня проекта:
```bash
uvicorn backend.app:app --reload
```
Сервер будет доступен по адресу: ``http://127.0.0.1:8000``

2️⃣ Frontend (Streamlit)

Запуск веб-интерфейса:
```bash
streamlit run frontend/app.py
```
Откроется браузер с интерфейсом
Можно выбрать тестовое видео из test/ или загрузить своё
