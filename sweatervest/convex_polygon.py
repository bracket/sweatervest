from .parser import register_class
from .util import reshape_vertices

import numpy as np


@register_class
class ConvexPolygon(object):
    def __init__(self, data):
        self.data = data

        vertices = np.array(data['vertices'], dtype=np.float32)
        self.vertices = reshape_vertices(vertices, data.get('color'))


    @classmethod
    def convert_to_object(cls, data):
        return ConvexPolygon(data)


    def convert_to_dict(self):
        return {
            '__class__' : 'ConvexPolygon',
            'vertices'  : self.vertices.tolist(),
        }
