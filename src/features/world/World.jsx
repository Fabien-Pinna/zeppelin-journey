import { assetUrl } from "../../assetUrl.js";
import { Suspense, useEffect, useState, useRef } from "react";
import { Canvas, useThree, useFrame } from "@react-three/fiber";
import { useTexture, Environment, useProgress } from "@react-three/drei";
import * as THREE from "three";
import { Scenery } from "./Scenery.jsx";
import { Journey } from "../journey/Journey.jsx";
import { createPendulum, stepPendulum } from "../journey/physics.js";
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
      <fog attach="fog" args={[night ? "#657b91" : "#d3d9c4", 90, 240]} />
      <hemisphereLight
        args={[night ? "#9eafda" : "#fff1d2", "#95a48e", night ? 0.9 : 1.8]}
      />
      <directionalLight
        position={[-35, 55, 35]}
        intensity={night ? 1 : 3}
        color={night ? "#b4c5f5" : "#ffe0ad"}
        castShadow
        shadow-mapSize={[2048, 2048]}
        shadow-camera-left={-60}
        shadow-camera-right={60}
        shadow-camera-top={60}
        shadow-camera-bottom={-60}
        shadow-camera-far={180}
        shadow-normalBias={0.12}
      />
      <directionalLight
        position={[30, 20, -30]}
        intensity={night ? 0.6 : 1}
        color="#c3e5ef"
      />
      <Environment resolution={64} frames={1} environmentIntensity={0.7}>
        <mesh scale={100}>
          <sphereGeometry args={[1, 16, 16]} />
          <meshBasicMaterial color="#ddd4ba" side={THREE.BackSide} />
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
