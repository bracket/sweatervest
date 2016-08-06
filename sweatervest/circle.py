from .parser import register_class
from .util import color_to_float
import numpy as np

default_position = (0, 0, 1, 1)

def convert_position(position):
    position = tuple(position) + default_position[len(position):]
    return np.array(position[:4], dtype=np.float32)


@register_class
class Circle(object):
    def __init__(self, data):
        self.center = convert_position(data['center'])
        self.radius = data['radius']
        self.color = np.array(color_to_float(data.get('color')), dtype=np.float32)
        self.data = data


    @classmethod
    def convert_to_object(cls, data):
        return Circle(data)


    def convert_to_dict(self):
        return {
            '__class__' : 'Circle',
            'color' : self.color.tolist(),
            'center' : self.center.tolist(),
            'radius' : self.radius,
        }
