"""Check shipped, decoded texture colors (requires Pillow); catch accidental double gamma conversion."""
import io
import json
import struct
from pathlib import Path
from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {'cliff': (201, 194, 177), 'grass': (119, 129, 90), 'wood': (150, 112, 73)}
checked = 0
for path in sorted((ROOT / 'public/models/world-v2').glob('*.glb')):
    data = path.read_bytes()
    length = struct.unpack_from('<I', data, 12)[0]
    gltf = json.loads(data[20:20 + length])
    binary = data[28 + length:]
    for material in gltf['materials']:
        name = material['name'].removeprefix('MAT-Journey-')
        if name not in EXPECTED:
            continue
        pbr = material['pbrMetallicRoughness']
        texture = gltf['textures'][pbr['baseColorTexture']['index']]
        image = gltf['images'][texture['extensions']['EXT_texture_webp']['source']]
        view = gltf['bufferViews'][image['bufferView']]
        start = view.get('byteOffset', 0)
        pixels = Image.open(io.BytesIO(binary[start:start + view['byteLength']])).convert('RGB')
        average = ImageStat.Stat(pixels).mean
        for actual, target in zip(average, EXPECTED[name]):
            assert .82 * target <= actual <= 1.06 * target, f'{path.name}: {name} color {average}'
        assert pbr.get('baseColorFactor', [1, 1, 1, 1]) == [1, 1, 1, 1], f'{path.name}: unintended color multiplier'
        checked += 1
assert checked >= 20, 'Expected shared stone, grass and timber maps across the chapter exports'
print(f'PASS: {checked} decoded WebP material colors retain the authored palette')
