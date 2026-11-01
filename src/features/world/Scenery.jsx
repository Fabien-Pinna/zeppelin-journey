import { useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import * as THREE from 'three';
import { Block, Pebble, Beam, Tree, Lantern } from './Primitives.jsx';
import { islands } from '../journey/world.js';

const IslandBase = ({ radius, color }) => <>
  <mesh position={[0, -0.35, 0]} receiveShadow><cylinderGeometry args={[radius, radius * 0.93, 0.75, 12]} /><meshStandardMaterial color={color} flatShading /></mesh>
  <mesh position={[0, -3.4, 0]} rotation={[Math.PI, 0, 0]} castShadow><coneGeometry args={[radius * 0.94, 6.3, 9, 2]} /><meshStandardMaterial color="#aa9183" flatShading /></mesh>
  {Array.from({ length: 9 }, (_, i) => {
    const a = i * 2.4;
    return <Pebble key={i} position={[Math.cos(a) * radius * 0.62, -2.4 - i % 3, Math.sin(a) * radius * 0.62]} scale={[2.5, 3, 2.4]} color={i % 2 ? '#bda38d' : '#8b8279'} detail={0} />;
  })}
  <mesh position={[2, 0.055, 2]} rotation={[-Math.PI / 2, 0, -0.6]} receiveShadow><circleGeometry args={[5.8, 32]} /><meshStandardMaterial color="#d8c699" /></mesh>
</>;

const Dock = ({ night }) => <group position={[6, 0, 5]} rotation={[0, -0.25, 0]}>
  {Array.from({ length: 13 }, (_, i) => <Block key={i} position={[0, 0.12, (i - 6) * 0.45]} size={[3.1, 0.22, 0.4]} color={i % 2 ? '#b48459' : '#c49b69'} />)}
  {[-1, 1].map((s) => <group key={s}>
    {[-2.8, 0, 2.8].map((z) => <Beam key={z} start={[s * 1.6, -1.4, z]} end={[s * 1.6, 0.8, z]} radius={0.12} />)}
    <Beam start={[s * 1.6, 0.7, -2.8]} end={[s * 1.6, 0.7, 2.8]} radius={0.035} color="#e5d3a5" />
  </group>)}
  <Lantern position={[1.65, 0.15, 2.7]} night={night} />
  <Block position={[-1.1, 0.55, -1.5]} size={[0.7, 0.7, 0.7]} color="#a5754e" />
</group>;

const Workshop = ({ night }) => <group position={[-3, 0, -3]}>
  <Block position={[0, 1.6, 0]} size={[4.8, 3.2, 3.5]} color="#eacb9b" />
  <mesh position={[0, 3.7, 0]} rotation={[0, Math.PI / 4, 0]} castShadow><coneGeometry args={[3.6, 1.8, 4]} /><meshStandardMaterial color="#bc7052" flatShading /></mesh>
  <Block position={[1.5, 4.2, -0.6]} size={[0.6, 1.6, 0.6]} color="#dab88c" />
  <Block position={[0, 1.3, 1.78]} size={[1, 2.6, 0.15]} color="#3f7275" />
  {[-1.5, 1.5].map(x => <group key={x}>
    <Block position={[x, 1.85, 1.8]} size={[1, 1.35, 0.15]} color="#486c6c" />
    <mesh position={[x, 1.85, 1.9]}><planeGeometry args={[0.75, 1.1]} /><meshStandardMaterial color="#ffe6ac" emissive="#ffd382" emissiveIntensity={night ? 1.3 : 0.15} /></mesh>
    <Block position={[x, 1.85, 1.92]} size={[0.07, 1.1, 0.04]} color="#e9c69b" />
  </group>)}
  <Block position={[0, 2.7, 2.8]} size={[5.5, 0.16, 2]} rotation={[0.15, 0, 0]} color="#538b87" />
  {[-2.5, 2.5].map(x => <Beam key={x} start={[x, 0, 3.5]} end={[x, 2.6, 3.5]} radius={0.08} />)}
  <Block position={[1.5, 0.9, 2.7]} size={[1.7, 0.15, 0.7]} color="#9b674c" />
  <Block position={[1.5, 1.3, 2.6]} size={[0.8, 0.6, 0.1]} color="#203f48" rotation={[-0.2, 0, 0]} />
  <Block position={[1.5, 1.3, 2.66]} size={[0.64, 0.44, 0.02]} color="#8fd5c3" rotation={[-0.2, 0, 0]} />
</group>;

const Bicycle = ({ position, rotation = 0 }) => <group position={position} rotation={[0, rotation, 0]}>
  {[-0.7, 0.7].map(x => <group key={x} position={[x, 0.55, 0]}>
    <mesh><torusGeometry args={[0.49, 0.045, 6, 20]} /><meshStandardMaterial color="#34474a" /></mesh>
    {[0, 1, 2, 3].map(i => <Beam key={i} start={[0, 0, 0]} end={[Math.cos(i * Math.PI / 2) * 0.47, Math.sin(i * Math.PI / 2) * 0.47, 0]} radius={0.012} color="#dbd3bb" />)}
  </group>)}
  {[ [[-0.7, 0.55, 0], [-0.2, 1.2, 0]], [[-0.2, 1.2, 0], [0.15, 0.55, 0]], [[0.15, 0.55, 0], [-0.7, 0.55, 0]], [[-0.2, 1.2, 0], [0.55, 1.2, 0]], [[0.55, 1.2, 0], [0.15, 0.55, 0]], [[0.55, 1.2, 0], [0.7, 0.55, 0]] ].map(([start, end], i) => <Beam key={i} start={start} end={end} radius={0.04} color="#cf8057" />)}
  <Block position={[-0.2, 1.27, 0]} size={[0.4, 0.1, 0.22]} color="#3e4b4a" />
  <Beam start={[0.55, 1.2, 0]} end={[0.55, 1.5, 0]} radius={0.04} />
  <Beam start={[0.55, 1.5, -0.25]} end={[0.55, 1.5, 0.25]} radius={0.04} />
</group>;

const TravelCamp = () => <>
  <group position={[-3, 0, -3]}>
    <Block position={[0, 1, 0]} size={[4, 2, 2.5]} color="#eee0b2" />
    <Block position={[0, 0.8, 1.26]} size={[4, 0.7, 0.08]} color="#6a9790" />
    <Block position={[0.5, 1.5, 1.3]} size={[1.2, 0.8, 0.08]} color="#507778" />
    <Block position={[-1, 1.1, 1.3]} size={[0.7, 1.7, 0.08]} color="#d8bd8a" />
    {[-1.3, 1.3].map(x => <mesh key={x} position={[x, 0.4, 1.2]} rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.4, 0.4, 0.25, 16]} /><meshStandardMaterial color="#394c4b" /></mesh>)}
    <Block position={[0, 2.1, 0]} size={[4.2, 0.25, 2.6]} color="#f1e1b8" />
  </group>
  <Bicycle position={[0, 0, 1]} rotation={0.4} /><Bicycle position={[-1, 0, 2.3]} rotation={0.2} />
  <Beam start={[2, 0, -4]} end={[2, 3, -4]} radius={0.1} />
  <Block position={[2, 2.7, -4]} size={[2.1, 0.55, 0.12]} color="#477b72" />
</>;

const Theatre = ({ reduced }) => {
  const swing = useRef();
  useFrame(({ clock }) => { if (swing.current) swing.current.rotation.z = reduced ? 0 : Math.sin(clock.elapsedTime * 1.4) * 0.35; });
  return <>
    <group position={[0, 0, -3]}>
      {Array.from({ length: 12 }, (_, i) => <mesh key={i} position={[0, 1.4, 0]} castShadow><cylinderGeometry args={[3.3, 3.3, 2.8, 1, 1, true, i * Math.PI / 6, Math.PI / 6]} /><meshStandardMaterial color={i % 2 ? '#f4deb0' : '#c76a64'} side={THREE.DoubleSide} /></mesh>)}
      {Array.from({ length: 12 }, (_, i) => <mesh key={i} position={[0, 3.6, 0]} castShadow><coneGeometry args={[3.7, 2.2, 1, 1, true, i * Math.PI / 6, Math.PI / 6]} /><meshStandardMaterial color={i % 2 ? '#ffe6b4' : '#d57b70'} side={THREE.DoubleSide} /></mesh>)}
      <Block position={[0, 1.2, 3.25]} size={[1.3, 2.4, 0.1]} color="#513e4b" />
      <Beam start={[0, 4.5, 0]} end={[0, 5.5, 0]} radius={0.05} />
      <Block position={[0.5, 5.3, 0]} size={[1, 0.4, 0.04]} color="#d59250" />
    </group>
    <group position={[-5, 0, 1]}>
      {[-1, 1].map(x => <Beam key={x} start={[x * 1.3, 0, 0]} end={[x * 1.3, 5, 0]} radius={0.09} color="#a97e57" />)}
      <Beam start={[-1.3, 5, 0]} end={[1.3, 5, 0]} radius={0.09} color="#a97e57" />
      <group ref={swing} position={[0, 5, 0]}>
        {[-0.6, 0.6].map(x => <Beam key={x} start={[x, 0, 0]} end={[x, -2.4, 0]} radius={0.02} />)}
        <Beam start={[-0.7, -2.4, 0]} end={[0.7, -2.4, 0]} radius={0.055} />
        <Pebble position={[0, -2.95, 0]} scale={[0.3, 0.5, 0.2]} color="#507e89" />
        <Pebble position={[0, -3.6, 0]} scale={[0.21, 0.23, 0.21]} color="#e4ad80" />
      </group>
    </group>
  </>;
};

const Flags = ({ night }) => <group>
  {[-7, 5].map(x => <Beam key={x} start={[x, 0, 2]} end={[x, 4, 2]} radius={0.06} />)}
  {Array.from({ length: 16 }, (_, i) => {
    const x = -7 + i * 0.8, y = 4 - Math.sin(i / 15 * Math.PI) * 1.15;
    return <group key={i}>
      {i < 15 && <Beam start={[x, y, 2]} end={[x + 0.8, 4 - Math.sin((i + 1) / 15 * Math.PI) * 1.15, 2]} radius={0.015} />}
      {i % 2 === 0 ? <mesh position={[x, y - 0.25, 2]} rotation={[0, 0, Math.PI]}><coneGeometry args={[0.23, 0.46, 3]} /><meshStandardMaterial color={['#d27964', '#e4bc66', '#629d95'][i % 3]} /></mesh> : <mesh position={[x, y - 0.1, 2]}><sphereGeometry args={[0.085, 8, 6]} /><meshStandardMaterial color="#ffe7ac" emissive="#ffc16c" emissiveIntensity={night ? 3 : 0.5} /></mesh>}
    </group>;
  })}
</group>;

const Person = ({ position, color, reduced, phase = 0 }) => {
  const ref = useRef();
  useFrame(({ clock }) => { if (ref.current && !reduced) ref.current.position.y = position[1] + Math.sin(clock.elapsedTime * 1.7 + phase) * 0.035; });
  return <group ref={ref} position={position}>
    <Pebble position={[0, 1.4, 0]} scale={[0.22, 0.25, 0.22]} color="#d6a37e" />
    <Block position={[0, 0.9, 0]} size={[0.47, 0.65, 0.32]} color={color} />
    {[-1, 1].map(s => <Block key={s} position={[s * 0.13, 0.35, 0]} size={[0.16, 0.65, 0.2]} color="#465964" />)}
  </group>;
};

const Clouds = () => {
  const clouds = useMemo(() => Array.from({ length: 24 }, (_, i) => ({ x: Math.sin(i * 7.3) * 83, y: -9 - i % 4 * 2, z: Math.cos(i * 4.7) * 75, scale: 3 + i % 4 })), []);
  return clouds.map((c, i) => <group key={i} position={[c.x, c.y, c.z]} scale={[c.scale * 1.7, c.scale * 0.55, c.scale]}>
    <Pebble position={[0, 0, 0]} color="#f6e3cc" /><Pebble position={[0.8, -0.2, 0]} scale={[0.9, 0.85, 0.85]} color="#f6e3cc" /><Pebble position={[-0.8, -0.2, 0]} scale={[0.8, 0.7, 0.8]} color="#f6e3cc" />
  </group>);
};

/** Hand-built archipelago, with one interactive exhibit per island. */
export const Scenery = ({ night, reduced, onExhibit, showLabels }) => <>
  <Clouds />
  {islands.map((island, i) => <group key={island.id} position={island.position}>
    <IslandBase radius={island.radius} color={i === 0 ? '#94aa7d' : i === 1 ? '#9eb383' : '#a7ac7f'} />
    <Dock night={night} />
    {i === 0 ? <Workshop night={night} /> : i === 1 ? <TravelCamp /> : <Theatre reduced={reduced} />}
    <Flags night={night} />
    <Tree position={[-7, 0, -4]} scale={1.2} autumn={i === 2} />
    <Tree position={[5, 0, -5]} scale={1.4} /><Tree position={[7, 0, -2]} scale={0.75} autumn={i === 0} />
    <Tree position={[-6, 0, 5]} scale={0.75} />
    <Lantern position={[2.5, 0, 1]} night={night} /><Lantern position={[-5, 0, 4]} night={night} />
    <Person position={[1, 0, -0.5]} color="#ba795c" reduced={reduced} phase={i} /><Person position={[-4, 0, 3]} color="#547d86" reduced={reduced} phase={i + 2} />
    {Array.from({ length: 16 }, (_, j) => {
      const a = j * 2.4, r = island.radius - 1.5;
      return <group key={j} position={[Math.cos(a) * r, 0, Math.sin(a) * r]}>
        <Pebble position={[0, 0.3, 0]} scale={[0.55, 0.4, 0.5]} color={j % 2 ? '#729775' : '#849f71'} />
        <Pebble position={[0.16, 0.65, 0.1]} scale={[0.13, 0.13, 0.13]} color={j % 2 ? '#f6cc6c' : '#e4a08c'} detail={0} />
      </group>;
    })}
    {showLabels && <Html position={[0, 2.5, 4]} center distanceFactor={25} zIndexRange={[10, 0]}><button className="world-label" onClick={() => onExhibit(island.id)}><span>{island.icon}</span> {island.short}<b>↗</b></button></Html>}
  </group>)}
</>;
