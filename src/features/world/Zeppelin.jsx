import { assetUrl } from "../../assetUrl.js";
import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import { useGLTF } from "@react-three/drei";
import { stepPropellers } from "../journey/flight.js";
import { scenicMaterial } from './materials.js';
/** Reworked passenger airship, sharing the dioramas' materials. */
export const Zeppelin = ({ flying, reduced, simulation }) => {
  const ref = useRef();
  const engine = useRef({ speed: 0, angle: 0, lastTime: null });
  const { scene } = useGLTF(assetUrl("models/world-v2/zeppelin.glb"));
  const { model, rotors } = useMemo(() => {
    const copy = scene.clone(true);
    const rotors = [];
    copy.traverse((o) => {
      if (/^ANIM-propeller-[LR](?:[._]?\d+)?$/.test(o.name)) rotors.push(o);
      if (o.isMesh) {
        o.material = scenicMaterial(o.material);
        o.castShadow = !o.material.transparent;
        o.receiveShadow = true;
      }
    });
    if (rotors.length !== 2) throw new Error("Les deux hélices du zeppelin sont introuvables.");
    return { model: copy, rotors };
  }, [scene]);
  useFrame(({ clock }) => {
    if (!ref.current) return;
    const time = simulation ? simulation.current.time : clock.elapsedTime;
    const delta = engine.current.lastTime === null ? 0 : time - engine.current.lastTime;
    engine.current.lastTime = time;
    const angle = stepPropellers(engine.current, delta, flying, reduced);
    rotors.forEach((rotor, index) => { rotor.rotation.z = angle * (index ? -1 : 1); });
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
