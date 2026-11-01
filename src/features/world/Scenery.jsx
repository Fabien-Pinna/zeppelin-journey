import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import { Html, useGLTF } from "@react-three/drei";
import { islands } from "../journey/world.js";
import { Avatar } from "../journey/Avatar.jsx";
useGLTF.setDecoderPath("/draco/");
const Diorama = ({ island, onExhibit, selected, overview }) => {
  const { scene } = useGLTF(`/models/world-v2/${island.id}.glb`);
  const model = useMemo(() => {
    const copy = scene.clone(true);
    copy.traverse((o) => {
      if (o.isMesh) {
        o.castShadow = true;
        o.receiveShadow = true;
      }
    });
    return copy;
  }, [scene]);
  return (
    <group position={island.position}>
      <primitive object={model} dispose={null} />
      {(selected || overview) && (
        <Html
          position={overview ? [0, 8, -3] : [2.5, 2.5, 3]}
          center
          distanceFactor={overview ? 55 : 20}
          zIndexRange={[10, 0]}
        >
          <button
            className={`world-label ${overview ? "distant-label" : ""}`}
            onPointerDown={(e) => e.stopPropagation()}
            onClick={() => onExhibit(island.id)}
          >
            <span>{island.number}</span>
            <b>{island.short}</b>
            <span>↗</span>
          </button>
        </Html>
      )}
    </group>
  );
};
const Stroller = ({ island, reduced, paused, onExhibit }) => {
  const ref = useRef(),
    time = useRef(0),
    motion = useRef({ speed: 0 });
  useFrame((_, dt) => {
    if (!ref.current) return;
    if (!paused && !reduced) time.current += Math.min(dt, 0.05);
    const t = time.current * 0.25;
    ref.current.position.set(
      island.position[0] - 4 + Math.sin(t) * 1.5,
      island.position[1] + 0.12,
      island.position[2] + 4.5,
    );
    ref.current.rotation.y = Math.cos(t) > 0 ? Math.PI / 2 : -Math.PI / 2;
    motion.current.speed = paused || reduced ? 0 : Math.abs(Math.cos(t)) * 0.35;
  });
  return (
    <group
      ref={ref}
      scale={0.9}
      onClick={(e) => {
        e.stopPropagation();
        onExhibit(island.id);
      }}
    >
      <Avatar
        motion={motion}
        reduced={reduced || paused}
        coat={island.id === "atelier" ? "#ac704d" : "#8b4b43"}
      />
    </group>
  );
};
export const Scenery = ({ onExhibit, islandId, mode, reduced, paused }) => (
  <>
    {islands.map((island) => (
      <Diorama
        key={island.id}
        island={island}
        onExhibit={onExhibit}
        selected={mode === "walking" && island.id === islandId}
        overview={
          mode === "overview" &&
          ["circus", "farm", "clubmed", "masonry"].includes(island.id)
        }
      />
    ))}
    {islands
      .filter((i) => ["atelier", "circus"].includes(i.id))
      .map((i) => (
        <Stroller
          key={i.id}
          island={i}
          reduced={reduced}
          paused={paused}
          onExhibit={onExhibit}
        />
      ))}
  </>
);
