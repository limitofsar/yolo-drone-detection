import torch
from ultralytics.nn.tasks import DetectionModel
from ultralytics.nn.modules.conv import Conv
from torch.nn.modules.container import Sequential
from torch.nn.modules.conv import Conv2d

# Список классов для safe_globals, чтобы загружать YOLO без ошибок
def enable_yolo_safe_load():
    torch.serialization.add_safe_globals([
        DetectionModel,
        Conv,
        Sequential,
        Conv2d
    ])
