__version__ = '0.1.0'

from .parser import parse_scene

# these need to be imported to register their class dispatchers to the parser
from .circle import Circle
from .group import Group
from .micropolygonmesh import MicropolygonMesh
from .scene import Scene
from .linepath import LinePath
