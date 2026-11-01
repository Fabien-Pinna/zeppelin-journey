import { useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import layouts from '../journey/layouts.json';
import { islands } from '../journey/world.js';

/** Concentrate shadow resolution on the current island; keep the overview's complete archipelago. */
export const Sunlight = ({ night, islandId, mode }) => {
  const target = useMemo(() => new THREE.Object3D(), []);
  const local = mode === 'walking';
  const center = local ? islands.find((island) => island.id === islandId).position : [-15, 3, -35];
  const span = local ? 29 : 90;
  return <group position={center}>
    <primitive object={target} />
    <directionalLight
      position={[-35, 48, 30]} target={target}
      intensity={night ? .65 : 3.6} color={night ? '#9cb8eb' : '#ffe2b4'}
      castShadow shadow-mapSize={[4096, 4096]}
      shadow-camera-left={-span} shadow-camera-right={span}
      shadow-camera-top={span} shadow-camera-bottom={-span}
      shadow-camera-near={.5} shadow-camera-far={220}
      shadow-bias={-.00008} shadow-normalBias={.035}
    />
  </group>;
};

/** A fixed pool of practical lights illuminates the nearest actual lanterns without unbounded GPU cost. */
export const LanternLighting = ({ night }) => {
  const lights = useRef([]);
  const points = useMemo(() => islands.flatMap((island) =>
    (layouts[island.id] || []).filter((item) => item.name === 'lantern').map((item) => ({
      position: new THREE.Vector3(
        island.position[0] + item.position[0],
        island.position[1] + item.size[1] - .23,
        island.position[2] + item.position[2],
      ), distance: 0,
    }))), []);
  useFrame(({ camera }) => {
    for (const point of points) point.distance = point.position.distanceToSquared(camera.position);
    points.sort((a, b) => a.distance - b.distance);
    lights.current.forEach((light, index) => {
      if (!light || !points[index]) return;
      light.position.copy(points[index].position);
      light.intensity = points[index].distance < 3600 ? (night ? 28 : 5) : 0;
    });
  });
  return Array.from({ length: 8 }, (_, index) => <pointLight
    key={index} ref={(light) => { lights.current[index] = light; }}
    color="#ffbd67" intensity={0} distance={8} decay={2}
  />);
};
