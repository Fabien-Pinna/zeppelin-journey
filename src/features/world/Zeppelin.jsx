import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Block, Beam } from './Primitives.jsx';

/** Gold and teal airship; local +Z points toward its nose. */
export const Zeppelin = ({ flying, reduced }) => {
  const propeller = useRef();
  useFrame((_, delta) => { if (propeller.current && !reduced) propeller.current.rotation.z += delta * (flying ? 22 : 3); });
  return <group>
    <mesh position={[0, 3.3, 0]} scale={[2, 1.85, 4.6]} castShadow><sphereGeometry args={[1, 32, 16]} /><meshStandardMaterial color="#e6b456" roughness={0.65} /></mesh>
    {[-2.9, -1.5, 0, 1.5, 2.9].map(z => {
      const r = Math.sqrt(1 - (z / 4.6) ** 2);
      return <mesh key={z} position={[0, 3.3, z]} scale={[2 * r, 1.85 * r, 1]}><torusGeometry args={[1.005, 0.015, 6, 40]} /><meshStandardMaterial color="#f7d388" metalness={0.3} roughness={0.5} /></mesh>;
    })}
    <mesh position={[0, 3.3, 0]} scale={[2.015, 1.87, 4.6]}><sphereGeometry args={[1, 32, 8, 0, Math.PI * 2, Math.PI * 0.59, Math.PI * 0.13]} /><meshStandardMaterial color="#478a89" /></mesh>
    <Block position={[0, 0.45, 0]} size={[1.55, 0.9, 3.5]} color="#d4a46c" />
    <Block position={[0, 0.95, 0.5]} size={[1.65, 0.18, 2.7]} color="#f3dfb0" />
    <Block position={[0, 0.55, 1.78]} size={[1.3, 0.55, 0.06]} color="#447d80" />
    {[-1, 1].map(s => <group key={s}>
      {[-1, 0, 1].map(z => <mesh key={z} position={[s * 0.79, 0.55, z]} rotation={[0, Math.PI / 2, 0]}><circleGeometry args={[0.21, 16]} /><meshStandardMaterial color="#31565c" metalness={0.3} roughness={0.3} /></mesh>)}
      {[-1.3, 1.3].map(z => <Beam key={z} start={[s * 0.7, 0.9, z]} end={[s * 1.25, 2.4, z]} radius={0.035} color="#8f7048" />)}
    </group>)}
    <Block position={[0, 3.5, -4.1]} size={[0.12, 2.9, 1.6]} rotation={[-0.3, 0, 0]} color="#468888" />
    <Block position={[0, 3.1, -4.1]} size={[3.2, 0.12, 1.3]} color="#468888" />
    <group ref={propeller} position={[0, 0.45, -2]}><Block size={[2.5, 0.14, 0.13]} color="#725c44" /><Block size={[0.14, 2.5, 0.13]} color="#725c44" /></group>
  </group>;
};
