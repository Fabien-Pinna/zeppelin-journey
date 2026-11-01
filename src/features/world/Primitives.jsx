import { useMemo } from 'react';
import * as THREE from 'three';

/** Shared soft, faceted building block for the miniature scenery. */
export const Block = ({ position, size = [1, 1, 1], color = '#eee1bd', rotation, ...props }) => <mesh castShadow receiveShadow position={position} rotation={rotation} {...props}><boxGeometry args={size} /><meshStandardMaterial color={color} roughness={0.85} /></mesh>;

/** Rounded low-poly shape. */
export const Pebble = ({ position, scale = [1, 1, 1], color = '#719b72', detail = 1, ...props }) => <mesh castShadow receiveShadow position={position} scale={scale} {...props}><icosahedronGeometry args={[1, detail]} /><meshStandardMaterial color={color} flatShading roughness={0.95} /></mesh>;

/** A cylinder between two endpoints, used for ropes, poles and frames. */
export const Beam = ({ start, end, radius = 0.04, color = '#765440' }) => {
  const { center, quaternion, length } = useMemo(() => {
    const a = new THREE.Vector3(...start), b = new THREE.Vector3(...end);
    const direction = b.clone().sub(a);
    return { center: a.add(b).multiplyScalar(0.5), length: direction.length(), quaternion: new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), direction.normalize()) };
  }, [start.join(), end.join()]);
  return <mesh position={center} quaternion={quaternion} castShadow><cylinderGeometry args={[radius, radius, length, 6]} /><meshStandardMaterial color={color} /></mesh>;
};

/** Stylized broadleaf tree with a visible forked trunk. */
export const Tree = ({ position, scale = 1, autumn = false }) => <group position={position} scale={scale}>
  <Beam start={[0, 0, 0]} end={[0.15, 2.6, 0]} radius={0.17} />
  <Beam start={[0, 1.5, 0]} end={[-0.9, 2.9, 0.2]} radius={0.1} />
  <Pebble position={[0, 3.25, 0]} scale={[1.45, 1.25, 1.3]} color={autumn ? '#d98d55' : '#537e69'} />
  <Pebble position={[-0.8, 2.8, 0.1]} scale={[0.9, 0.85, 1]} color={autumn ? '#edb365' : '#7fa37a'} />
  <Pebble position={[0.7, 3.2, 0.5]} scale={[1, 0.9, 0.9]} color={autumn ? '#e8a459' : '#95b37b'} />
</group>;

/** Warm emissive lantern with an unlit metal frame. */
export const Lantern = ({ position, night }) => <group position={position}>
  <Beam start={[0, 0, 0]} end={[0, 2.2, 0]} radius={0.065} color="#384d4d" />
  <Block position={[0, 2.2, 0]} size={[0.36, 0.12, 0.36]} color="#384d4d" />
  <mesh position={[0, 1.93, 0]}><boxGeometry args={[0.24, 0.45, 0.24]} /><meshStandardMaterial color="#ffe3a0" emissive="#ffb455" emissiveIntensity={night ? 2.5 : 0.4} /></mesh>
  <Block position={[0, 1.68, 0]} size={[0.34, 0.1, 0.34]} color="#384d4d" />
</group>;
