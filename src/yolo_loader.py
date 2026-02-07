from ultralytics import YOLO
from .safe_load import enable_yolo_safe_load

enable_yolo_safe_load()

# Словарь для кэширования моделей
_loaded_models = {}

def load_model(name, path):
    '''
    Загружает модель и кэширует её.
    Если модель уже загружена - возвращает из кэша.
    '''
    if name not in _loaded_models:
        _loaded_models[name] = YOLO(path)
    return _loaded_models[name]

# Предустанавливаем модели
DEFAULT_MODEL = 'YOLOv8n'
MODELS = {
    'YOLOv8n': 'model_weights/YOLOv8n.pt',  # быстрая модель
    'YOLOv8m': 'model_weights/YOLOv8m.pt',  # тяжелая модель
}

def get_model(model_name: str=DEFAULT_MODEL):
    '''
    Возвращает объект YOLO модели.
    По умолчанию возвращает быструю модель.
    '''
    if model_name not in MODELS:
        raise ValueError(f'Модель {model_name} не найдена. Доступны: {list(MODELS.keys())}')
    return load_model(model_name, MODELS[model_name])

def available_models():
    return list(MODELS.keys())

