# SweaterVest

**Scene graph description language for Victor and Handsome projects**

## Overview

SweaterVest is a Python-based scene graph description language that uses YAML as its input format. It provides a simple and declarative way to describe 2D scenes with geometric primitives, paths, and hierarchical transformations. The library parses YAML scene descriptions and converts them into a structured object model that can be used by rendering engines and graphical applications.

## What is a Scene Graph?

A scene graph is a hierarchical data structure that organizes the logical and spatial representation of a graphical scene. In SweaterVest, scene graphs consist of:

- **Scene**: The root container with canvas configuration
- **Groups**: Hierarchical nodes that can contain children and apply transformations
- **Primitives**: Geometric shapes and paths (circles, polygons, meshes, paths)

This structure allows for efficient scene management, transformation inheritance, and modular composition of complex graphics.

## YAML Format

SweaterVest uses YAML with a special `__class__` field to specify object types. Here's a simple example:

```yaml
{
    "__class__": "Scene",
    "canvas": {
        "extents": [512, 512],
        "color": "white"
    },
    "top": {
        "__class__": "Group",
        "transformation": [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ],
        "children": [
            {
                "__class__": "Circle",
                "center": [256, 256],
                "radius": 50,
                "color": "#ff0000"
            }
        ]
    }
}
```

### Color Format

Colors can be specified in several formats:
- Hex strings: `"#ff0000"`, `"#f00"`, `"#ff0000ff"` (with alpha)
- RGB/RGBA tuples: `[255, 0, 0]` or `[255, 0, 0, 255]`
- Integer values (0-255) or float values (0.0-1.0)

### Vertex Format

Vertices are specified as arrays with flexible dimensions:
- 2D: `[x, y]` - automatically expanded to `[x, y, 1, 1]`
- 3D: `[x, y, z]` - automatically expanded to `[x, y, z, 1]`
- 4D: `[x, y, z, w]` - homogeneous coordinates
- 8D: `[x, y, z, w, r, g, b, a]` - position with color

## Main Classes

### Scene
The root container for a scene graph. Contains canvas configuration and a top-level group.

**Attributes:**
- `data`: Dictionary containing canvas settings and top-level group

### Group
Hierarchical container that can hold children (other groups or primitives) and apply transformations.

**Attributes:**
- `xform`: Optional 4x4 transformation matrix (numpy array)
- `children`: List of child scene graph objects

### Circle
A circular primitive defined by center point and radius.

**Attributes:**
- `center`: Center position as 4D vector `[x, y, z, w]`
- `radius`: Circle radius (float)
- `color`: RGBA color as float array

### ConvexPolygon
A convex polygon defined by its vertices.

**Attributes:**
- `vertices`: Vertex array with shape `(n, 8)` containing position and color data

### LinePath
A path composed of connected line segments.

**Attributes:**
- `vertices`: Vertex array with shape `(n, 8)` containing position and color data

### CubicHermitePath
A smooth path using cubic Hermite interpolation.

**Attributes:**
- `vertices`: Control points with shape `(n, 8)` containing position and color data

### MicropolygonMesh
A mesh of micropolygons for rendering complex surfaces.

**Attributes:**
- `vertices`: 2D or 3D vertex array with shape `(rows, cols, 8)` or `(n, 8)`

## Installation

### Requirements
- Python 2.6+ or Python 3.3+
- numpy
- pyyaml

### Install from source

```bash
pip install -r requirements.txt
pip install -e .
```

## Basic Usage

### Parsing a Scene

```python
from sweatervest import parse_scene

# Parse from file
scene = parse_scene('path/to/scene.yaml')

# Parse from file object
with open('path/to/scene.yaml') as f:
    scene = parse_scene(f)
```

### Working with Scene Objects

```python
# Access scene data
canvas = scene.data['canvas']
top_group = scene.data['top']

# Iterate through group children
for child in top_group.children:
    print(type(child).__name__)

# Convert back to dictionary format
scene_dict = scene.convert_to_dict()
```

### Creating Scene Objects Programmatically

All scene graph objects can be created programmatically:

```python
from sweatervest import Circle, Group, Scene
import numpy as np

# Create a circle
circle_data = {
    'center': [100, 100],
    'radius': 25,
    'color': '#00ff00'
}
circle = Circle(circle_data)

# Create a group with transformation
group_data = {
    'transformation': np.eye(4).tolist(),
    'children': [circle]
}
group = Group(group_data)
```

## Architecture

SweaterVest follows a simple parser-converter architecture:

1. **YAML Parsing** (`parser.py`): Reads YAML files and converts them to Python dictionaries
2. **Object Conversion** (`parser.py`): Recursively converts dictionaries to registered class instances
3. **Class Registration** (`parser.py`): Classes register themselves using the `@register_class` decorator
4. **Object Model** (various modules): Each class implements `convert_to_object()` and `convert_to_dict()` methods

The parser uses a registry pattern where each scene graph class is decorated with `@register_class`, which maps the class name to its constructor. When parsing YAML, the `__class__` field determines which class to instantiate.

## Key Files

- [`sweatervest/parser.py`](sweatervest/parser.py) - Core parsing and conversion logic
- [`sweatervest/scene.py`](sweatervest/scene.py) - Scene root class
- [`sweatervest/group.py`](sweatervest/group.py) - Hierarchical group node
- [`sweatervest/circle.py`](sweatervest/circle.py) - Circle primitive
- [`sweatervest/convex_polygon.py`](sweatervest/convex_polygon.py) - Convex polygon primitive
- [`sweatervest/linepath.py`](sweatervest/linepath.py) - Line path primitive
- [`sweatervest/cubic_hermite_path.py`](sweatervest/cubic_hermite_path.py) - Cubic Hermite path
- [`sweatervest/micropolygonmesh.py`](sweatervest/micropolygonmesh.py) - Micropolygon mesh
- [`sweatervest/util.py`](sweatervest/util.py) - Utility functions for color and vertex processing
- [`tests/data/test_scene.yaml`](tests/data/test_scene.yaml) - Example scene file

## License

See [LICENSE](LICENSE) file for details.

## Author

Stephen [Bracket] McCray (mcbracket@gmail.com)
