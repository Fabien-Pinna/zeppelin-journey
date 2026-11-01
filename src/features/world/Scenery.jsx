import { assetUrl } from "../../assetUrl.js";
import { useMemo } from "react";
import { Html, useGLTF } from "@react-three/drei";
import { islands } from "../journey/world.js";
import { Activity, Guide, useScenicMotion } from "./Life.jsx";
import { scenicMaterial } from './materials.js';
useGLTF.setDecoderPath(assetUrl("draco/"));
const Diorama = ({
  island,
  onExhibit,
  onTalk,
  selected,
  overview,
  alive,
  simulation,
}) => {
  const { scene } = useGLTF(assetUrl(`models/world-v2/${island.id}.glb`));
  const model = useMemo(() => {
    const copy = scene.clone(true);
    copy.traverse((o) => {
      if (o.isMesh) {
        o.material = scenicMaterial(o.material);
        o.castShadow = !o.material.transparent;
        o.receiveShadow = true;
      }
    });
    return copy;
  }, [scene]);
  useScenicMotion(model, simulation);
  return (
    <group position={island.position}>
      <primitive object={model} dispose={null} />
      {alive && <Activity id={island.id} simulation={simulation} />}
      {selected && (
        <Guide island={island} simulation={simulation} onTalk={onTalk} />
      )}
      {overview && (
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
export const Scenery = ({ onExhibit, onTalk, islandId, mode, simulation }) => (
  <>
    {islands.map((island) => (
      <Diorama
        key={island.id}
        island={island}
        onExhibit={onExhibit}
        onTalk={onTalk}
        simulation={simulation}
        alive
        selected={mode === "walking" && island.id === islandId}
        overview={
          mode === "overview" &&
          ["circus", "farm", "clubmed", "masonry"].includes(island.id)
        }
      />
    ))}
  </>
);
