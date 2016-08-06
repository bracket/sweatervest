from .parser import register_class
from .util import color_to_float

import numpy as np

@register_class
class MicropolygonMesh(object):
    def __init__(self, data):
        self.data = data

        vertices = np.array(
            data['vertices'],
            dtype=np.float32,
        )

        self.vertices = self.reshape_input(vertices, data.get('color'))


    def reshape_input(self, input, color=None):
        if len(input.shape) != 3:
            raise RuntimeError('input must have shape of length 3')

        dimension = input.shape[2]

        if dimension > 8:
            raise RuntimeError('input dimension too high')

        if dimension == 8:
            return input

        shape = list(input.shape)
        shape[2] = 8

        out = np.zeros(shape=shape, dtype=np.float32)
        out[:,:,:dimension] = input

        if dimension < 3:
            out[:,:,2] = 1

        if dimension < 4:
            out[:,:,3] = 1

        out[:,:,4:] = color_to_float(color)

        return out


    @classmethod
    def convert_to_object(cls, data):
        return MicropolygonMesh(data)


    def convert_to_dict(self):
        out = {
            '__class__' : 'MicropolygonMesh',
            'vertices'  : self.vertices.tolist(),
        }

        return out
