"""Compress exported PBR maps, then encode geometry once; never re-encode an existing Draco asset."""
import argparse
import concurrent.futures
import json
import struct
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--only',nargs='*')
args=parser.parse_args()
source=ROOT/'artifacts/art-rebuild/candidates'
output=ROOT/'artifacts/art-rebuild/optimized'
output.mkdir(parents=True,exist_ok=True)
assets=[source/(name+'.glb') for name in args.only] if args.only else sorted(source.glob('*.glb'))

def gltf(path):
    data=path.read_bytes()
    return json.loads(data[20:20+struct.unpack_from('<I',data,12)[0]])

def run(*command):
    result=subprocess.run(['npm.cmd','exec','--yes','--package','@gltf-transform/cli@4.5.1','--','gltf-transform',*map(str,command)],cwd=ROOT,capture_output=True,text=True)
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)

def prepare(path):
    raw=gltf(path)
    assert 'KHR_draco_mesh_compression' not in raw.get('extensionsUsed',[]), f'{path}: expected raw geometry'
    intermediate=output/(path.stem+'.webp.glb')
    final=output/path.name
    run('webp',path,intermediate,'--quality','92','--effort','50')
    run('draco',intermediate,final)
    result=gltf(final)
    assert 'KHR_draco_mesh_compression' in result.get('extensionsUsed',[])
    assert 'EXT_texture_webp' in result.get('extensionsUsed',[])
    intermediate.unlink()
    report={'asset':path.name,'raw_bytes':path.stat().st_size,'bytes':final.stat().st_size,
            'triangles':sum(result['accessors'][p['indices']]['count']//3 for m in result['meshes'] for p in m['primitives']),
            'materials':len(result.get('materials',[])), 'images':len(result.get('images',[]))}
    print(json.dumps(report),flush=True)
    return report

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    reports=list(executor.map(prepare,assets))
(output/'manifest.json').write_text(json.dumps(reports,indent=2)+'\n')
print('ART_PREPARE_COMPLETE',sum(report['bytes'] for report in reports),flush=True)
