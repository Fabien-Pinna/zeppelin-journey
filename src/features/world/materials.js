import * as THREE from 'three';

const shared = new Map();

/** Reuse the identical exported palette across chapters instead of uploading its maps nine times. */
export function scenicMaterial(material) {
  if (!material.name.startsWith('MAT-Journey-')) return material;
  if (shared.has(material.name)) return shared.get(material.name);
  for (const slot of ['map', 'normalMap', 'roughnessMap', 'metalnessMap']) {
    if (material[slot]) material[slot].anisotropy = 4;
  }
  if (material.transparent) {
    material.depthWrite = false;
    material.side = THREE.DoubleSide;
  }
  shared.set(material.name, material);
  return material;
}
