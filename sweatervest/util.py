import numpy as np

def make_color_grammar():
    import re

    g = { }
    
    g['digit']      = r'[0-9a-fA-F]'
    g['ddigit']     = r'(?:{digit}{{2}})'.format(**g)
    g['hex_color']  = r'^#?(?:(?P<double>{ddigit}{{3,4}})|(?P<single>{digit}{{3,4}}))$'.format(**g)

    for key, value in g.items():
        g[key] = re.compile(value)

    return g

color_grammar = make_color_grammar()

def parse_color(string):
    m = color_grammar['hex_color'].match(string)

    if m is None:
        return None

    single = m.group('single')
    if single is not None:
        R, G, B = single[0], single[1], single[2]
        A = 'f' if len(single) == 3 else single[3]
        return tuple(int(2*v, 16) for v in (R, G, B, A))

    double = m.group('double')
    if double is not None:
        R, G, B = double[0:2], double[2:4], double[4:6]
        A = 'ff' if len(double) == 6 else double[6:8]
        return tuple(int(v, 16) for v in (R, G, B, A))


def color_to_float(color):
    if color is None:
        return (0., 0., 0., 0.)
    elif isinstance(color, str):
        return tuple(c / 255. for c in parse_color(color))
    else:
        return tuple(c / 255. if isinstance(c, int) else c for c in color)


def reshape_vertices(input, color=None):
    shape = list(input.shape)

    if len(shape) == 2:
        dimension = shape[1]
        shape[1] = 8

        slice_at = lambda x: np.s_[:,x]
        slice_to = lambda x: np.s_[:,:x]
        slice_from = lambda x: np.s_[:,x:]
    elif len(shape) == 3:
        dimension = shape[2]
        shape[2] = 8

        slice_at = lambda x: np.s_[:,:,x]
        slice_to = lambda x: np.s_[:,:,:x]
        slice_from = lambda x: np.s_[:,:,x:]
    else:
        raise RuntimeError(
            'input must have shape of length 2 or 3',
            { 'shape' : shape }
        )

    valid = (2, 3, 4, 8)
    if dimension not in valid:
        raise RuntimeError(
            'invalid input dimension',
            { 'dimension' : dimension, 'valid' : valid }
        )

    if dimension == 8:
        return input

    out = np.zeros(shape=shape, dtype=np.float32)
    out[slice_to(dimension)] = input

    if dimension < 3:
        out[slice_at(2)] = 1

    if dimension < 4:
        out[slice_at(3)] = 1

    out[slice_from(4)] = color_to_float(color)

    return out
