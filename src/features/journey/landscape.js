import landscapes from './landscapes.json' with { type: 'json' };
export { landscapes };

/** Same superellipse shoreline contract as the exported Blender terrain. */
export function islandBoundary(id, angle) {
  const shape = landscapes[id];
  const ellipse = (Math.abs(Math.cos(angle) / shape.rx) ** shape.power + Math.abs(Math.sin(angle) / shape.rz) ** shape.power) ** (-1 / shape.power);
  return ellipse * (1 + shape.scallop * Math.cos(3 * angle + shape.phase));
}
