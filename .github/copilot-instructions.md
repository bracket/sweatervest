# GitHub Copilot Instructions for SweaterVest

## Project Overview

SweaterVest is a scene graph description language that bridges YAML declarative descriptions with Python object models. The project enables users to define 2D graphical scenes in YAML format and convert them into structured Python objects for use in rendering engines like Victor and Handsome.

### Core Concepts

- **Scene Graph**: Hierarchical structure organizing graphical elements
- **YAML-to-Object Conversion**: Declarative YAML input → Python object model
- **Registry Pattern**: Classes self-register with the parser using decorators
- **Flexible Vertex Format**: Automatic expansion of vertex data (2D→3D→4D→8D)
- **Color Handling**: Support for hex strings, RGB/RGBA tuples, and mixed int/float values

## Architecture

### Module Organization

```
sweatervest/
├── parser.py           # Core: YAML parsing, object conversion, class registry
├── scene.py            # Root container with canvas configuration
├── group.py            # Hierarchical container with transformations
├── circle.py           # Circle primitive
├── convex_polygon.py   # Convex polygon primitive
├── linepath.py         # Line path primitive
├── cubic_hermite_path.py  # Cubic Hermite path primitive
├── micropolygonmesh.py    # Micropolygon mesh
└── util.py             # Color parsing and vertex reshaping utilities
```

### Key Design Patterns

#### Registry Pattern
Classes register themselves with the parser using the `@register_class` decorator:

```python
from .parser import register_class

@register_class
class MyShape(object):
    @classmethod
    def convert_to_object(cls, data):
        return MyShape(data)
    
    def convert_to_dict(self):
        return {'__class__': 'MyShape', ...}
```

#### Two-Way Conversion
All scene graph objects support bidirectional conversion:
- `convert_to_object(data)`: Class method that creates instances from dictionaries
- `convert_to_dict()`: Instance method that serializes back to dictionary format

#### Recursive Object Conversion
The parser recursively traverses dictionaries and lists, converting any dictionary with a `__class__` field into the corresponding registered class instance.

## Code Style and Conventions

### General Guidelines

1. **Minimal Dependencies**: Use only numpy and pyyaml
2. **NumPy Arrays**: Store vertex and color data as `np.float32` arrays
3. **Data Attribute**: Keep original input in `self.data` for reference
4. **Transformation Matrices**: Use 4x4 homogeneous transformation matrices
5. **Color Format**: Store colors as RGBA float arrays (0.0-1.0 range)

### Naming Conventions

- **Classes**: PascalCase (e.g., `ConvexPolygon`, `CubicHermitePath`)
- **Functions**: snake_case (e.g., `parse_scene`, `color_to_float`)
- **Private Functions**: Prefix with underscore (not used in current codebase)
- **Class Methods**: `convert_to_object`, `convert_to_dict` for serialization

### Vertex Data Format

Standard 8-element vertex format: `[x, y, z, w, r, g, b, a]`
- Position: `[x, y, z, w]` (homogeneous coordinates)
- Color: `[r, g, b, a]` (RGBA floats 0.0-1.0)

Use `reshape_vertices()` from `util.py` to automatically expand shorter formats.

## Extending the Scene Graph

### Adding a New Shape Type

To add a new geometric primitive or scene element:

1. **Create a new module** in `sweatervest/` (e.g., `rectangle.py`)

2. **Implement the shape class**:
   ```python
   from .parser import register_class
   import numpy as np
   
   @register_class
   class Rectangle(object):
       def __init__(self, data):
           self.data = data
           # Parse and store shape-specific data
           self.position = np.array(data['position'], dtype=np.float32)
           self.size = np.array(data['size'], dtype=np.float32)
           # Use utility functions from util.py for colors
           from .util import color_to_float
           self.color = np.array(color_to_float(data.get('color')), dtype=np.float32)
       
       @classmethod
       def convert_to_object(cls, data):
           return Rectangle(data)
       
       def convert_to_dict(self):
           return {
               '__class__': 'Rectangle',
               'position': self.position.tolist(),
               'size': self.size.tolist(),
               'color': self.color.tolist(),
           }
   ```

3. **Import in `__init__.py`**: Add the import so the class registers at module load:
   ```python
   from .rectangle import Rectangle
   ```

4. **Use in YAML**:
   ```yaml
   {
       "__class__": "Rectangle",
       "position": [100, 100],
       "size": [50, 30],
       "color": "#ff0000"
   }
   ```

### Utility Functions

When adding new shapes, leverage existing utilities:

- `color_to_float(color)`: Convert hex/int/float colors to RGBA float tuple
- `reshape_vertices(input, color)`: Expand vertex arrays to 8D format
- `parse_color(string)`: Parse hex color strings to RGBA int tuple

### Testing New Features

Follow existing test patterns:

```python
from pathlib import Path
import sweatervest

def test_new_shape():
    from sweatervest.parser import parse_scene
    
    path = Path(__file__).parent / 'data' / 'test_shape.yaml'
    scene = parse_scene(str(path))
    
    # Verify scene structure
    assert isinstance(scene, sweatervest.scene.Scene)
    
    # Check shape properties
    shape = scene.data['top'].children[0]
    assert isinstance(shape, sweatervest.rectangle.Rectangle)
```

## Development Practices

### Code Organization

- **One class per file**: Each shape/primitive gets its own module
- **Register at module level**: Use `@register_class` decorator on class definition
- **Import in `__init__.py`**: Ensure classes are imported so registration happens

### Data Validation

- **Graceful defaults**: Use `.get('key', default)` for optional fields
- **Type conversion**: Always convert to numpy arrays with explicit dtype
- **Shape validation**: Validate array dimensions where appropriate

### Error Handling

- Use `RuntimeError` for invalid input shapes or dimensions
- Include helpful context in error messages (see `util.py` examples)
- Validate vertex dimensions early in constructors

### Testing Expectations

1. **Parser tests**: Verify YAML files parse correctly into expected object types
2. **Utility tests**: Test color parsing and vertex reshaping with various inputs
3. **Round-trip tests**: Ensure `convert_to_dict()` → `convert_to_object()` preserves data
4. **Example data**: Create test YAML files in `tests/data/` for new features

### Dependencies

- **NumPy**: For array operations and numerical data
- **PyYAML**: For YAML parsing (note: using deprecated `yaml.load()` without Loader)
- **No additional dependencies**: Keep the project lightweight

## Common Patterns

### Handling Optional Fields

```python
def __init__(self, data):
    self.data = data
    self.color = color_to_float(data.get('color'))  # Returns default if None
    
    xform = data.get('transformation', None)
    if xform is None:
        self.xform = None
    else:
        self.xform = np.array(xform, dtype=np.float32)
```

### Working with Vertex Arrays

```python
# Input: flexible dimension array
vertices = np.array(data['vertices'], dtype=np.float32)

# Output: always 8-element format
self.vertices = reshape_vertices(vertices, data.get('color'))
```

### Serialization

```python
def convert_to_dict(self):
    out = {'__class__': self.__class__.__name__}
    
    # Convert numpy arrays to lists for YAML serialization
    if self.xform is not None:
        out['transformation'] = self.xform.tolist()
    
    # Recursively serialize children
    out['children'] = [child.convert_to_dict() for child in self.children]
    
    return out
```

## Key Relationships

### Parser → Classes
The parser maintains a registry (`parser_classes` dict) mapping class names to class objects. When parsing, it looks up the `__class__` field and calls the appropriate `convert_to_object()` method.

### Scene → Group → Primitives
Scenes contain a root Group, Groups contain children (which can be Groups or primitives), primitives are leaves in the tree.

### Util → All Shape Classes
All shape classes depend on `util.py` for color and vertex processing. Don't duplicate this logic.

## Important Notes

- **YAML Security**: The codebase uses deprecated `yaml.load()` without a Loader argument, which is a security risk. Consider using `yaml.safe_load()` in future work.
- **Python 2/3 Compatibility**: The project targets Python 2.6+ and 3.3+, so avoid Python 3-only syntax.
- **Scratch Directory**: Files in `scratch/` are not part of the main codebase and should be ignored.
- **No Modification Policy**: Avoid breaking changes to the API. The project is used by Victor and Handsome rendering engines.

## Quick Reference

### File Locations
- Source code: `sweatervest/*.py`
- Tests: `tests/test_*.py`
- Test data: `tests/data/*.yaml`
- Setup: `setup.py`, `requirements.txt`

### Common Tasks
- **Add new shape**: Create module, register class, import in `__init__.py`
- **Parse scene**: `from sweatervest import parse_scene; scene = parse_scene('file.yaml')`
- **Run tests**: `pytest tests/` (or appropriate test runner)
- **Check dependencies**: See `requirements.txt`

### Best Practices
- Use utility functions for colors and vertices
- Follow the registry pattern for new classes
- Implement both `convert_to_object()` and `convert_to_dict()`
- Store original data in `self.data`
- Convert to numpy arrays with explicit dtype
- Add tests for new features
