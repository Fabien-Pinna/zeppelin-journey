import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import { useGLTF } from "@react-three/drei";
/** Reworked passenger airship, sharing the dioramas' materials. */
export const Zeppelin = ({ flying, reduced, simulation }) => {
  const ref = useRef();
  const { scene } = useGLTF("/models/world-v2/zeppelin.glb");
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
  useFrame(({ clock }) => {
    if (!ref.current) return;
    const time = simulation ? simulation.current.time : clock.elapsedTime;
    ref.current.position.y = reduced
      ? 0
      : Math.sin(time * 0.7) * (flying ? 0.12 : 0.05);
    ref.current.rotation.z = reduced ? 0 : Math.sin(time * 0.45) * 0.008;
  });
  return (
    <group ref={ref}>
      <primitive object={model} dispose={null} />
    </group>
  );
};
