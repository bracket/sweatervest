from pathlib import Path
import sweatervest

def test_parse_scene():
    from sweatervest.parser import parse_scene

    path = Path(__file__).parent / 'data' / 'test_scene.yaml'
    scene = parse_scene(str(path))
    assert isinstance(scene, sweatervest.scene.Scene)
