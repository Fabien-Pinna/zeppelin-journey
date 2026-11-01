import { assetUrl } from "../../assetUrl.js";
import { Suspense, useEffect, useState, useRef } from "react";
import { Canvas, useThree, useFrame } from "@react-three/fiber";
import { useTexture, Environment, useProgress } from "@react-three/drei";
import * as THREE from "three";
import { Scenery } from "./Scenery.jsx";
import { Journey } from "../journey/Journey.jsx";
import { createPendulum, stepPendulum } from "../journey/physics.js";
import { Sunlight, LanternLighting } from './Lighting.jsx';
const Simulation = ({ simulation, paused, reduced }) => {
  useFrame((_, delta) => {
    if (!paused && !reduced) {
      simulation.current.time += Math.min(delta, 0.05);
      stepPendulum(simulation.current.pendulum, delta);
    }
  }, -10);
  return null;
};
const Atmosphere = ({ night }) => {
  const skies = useTexture([
    assetUrl("textures/cloud-sea.png"),
    assetUrl("textures/cloud-sea-evening.png"),
  ]);
  const sky = skies[night ? 1 : 0];
  const { scene, size } = useThree();
  useEffect(() => {
    sky.colorSpace = THREE.SRGBColorSpace;
    const scale = Math.min(1, size.width / size.height / 2);
    sky.repeat.set(scale, 1);
    sky.offset.set((1 - scale) / 2, 0);
    scene.background = sky;
    return () => {
      scene.background = null;
    };
  }, [scene, sky, size.width, size.height]);
  return (
    <>
      <fog attach="fog" args={[night ? "#51698b" : "#b4c6d2", 65, 220]} />
      <hemisphereLight
        args={[night ? "#8eabda" : "#cedfec", "#a99b7f", night ? 0.5 : 1.05]}
      />
      <directionalLight
        position={[30, 20, -30]}
        intensity={night ? 0.35 : .55}
        color="#c3e5ef"
      />
      <Environment key={night ? 'evening' : 'day'} resolution={128} frames={1} environmentIntensity={night ? .25 : .45}>
        <mesh scale={100}>
          <sphereGeometry args={[1, 16, 16]} />
          <meshBasicMaterial color={night ? '#617899' : '#b8d0df'} side={THREE.BackSide} />
        </mesh>
        <mesh position={[-15, 25, 10]} rotation={[Math.PI / 2, .3, 0]}>
          <planeGeometry args={[30, 20]} />
          <meshBasicMaterial color={night ? '#acb9d4' : '#fff0d5'} side={THREE.DoubleSide} toneMapped={false} />
        </mesh>
        <mesh position={[0, -20, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[80, 80]} />
          <meshBasicMaterial color="#625a45" side={THREE.DoubleSide} />
        </mesh>
      </Environment>
    </>
  );
};
const Loading = () => {
  const { progress } = useProgress();
  return (
    <div className="loading" role="status">
      <span className="loading-orbit">✦</span>
      <b>L’archipel se prépare</b>
      <span>{Math.round(progress)} % · Chargement des décors</span>
    </div>
  );
};
const Ready = ({ onReady }) => {
  useEffect(() => {
    onReady(true);
  }, [onReady]);
  return null;
};

export const World = (props) => {
  const [ready, setReady] = useState(false);
  const simulation = useRef({
    time: 0,
    pendulum: createPendulum(),
    player: [7, 0.2, 8],
  });
  return (
    <>
      <Canvas
        shadows={{ type: THREE.PCFShadowMap }}
        dpr={[1, 1.5]}
        camera={{ position: [30, 24, 43], fov: 45, near: 0.1, far: 350 }}
        gl={{
          antialias: true,
          powerPreference: "high-performance",
          toneMapping: THREE.ACESFilmicToneMapping,
          toneMappingExposure: 1.05,
        }}
        fallback={
          <div className="canvas-fallback">
            Archipel en 3D. Le carnet propose une version accessible des neuf
            escales.
          </div>
        }
      >
        <Suspense fallback={null}>
          <Atmosphere night={props.night} />
          <Sunlight night={props.night} islandId={props.islandId} mode={props.mode} />
          <LanternLighting night={props.night} />
          <Simulation
            simulation={simulation}
            paused={props.paused}
            reduced={props.reduced}
          />
          <Scenery
            onExhibit={props.onExhibit}
            onTalk={props.onTalk}
            simulation={simulation}
            islandId={props.islandId}
            mode={props.mode}
            reduced={props.reduced}
            paused={props.paused}
          />
          <Journey {...props} simulation={simulation} />
          <Ready onReady={setReady} />
        </Suspense>
      </Canvas>
      {!ready && <Loading />}
    </>
  );
};
