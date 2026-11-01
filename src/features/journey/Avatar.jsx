import { useMemo } from "react";
import { useGLTF } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
/** Original Blender-authored character, with independent runtime joints. */
export const Avatar = ({ motion, reduced, coat }) => {
  const { scene } = useGLTF("/models/world-v2/traveller.glb");
  const { model, joints } = useMemo(() => {
    const model = scene.clone(true),
      joints = {};
    model.traverse((o) => {
      if (o.isMesh) {
        o.castShadow = true;
        if (coat && o.name.includes("-teal")) {
          o.material = o.material.clone();
          o.material.map = null;
          o.material.color.set(coat);
        }
      }
      if (
        ["LeftArm", "RightArm", "LeftLeg", "RightLeg", "Head"].includes(o.name)
      )
        joints[o.name] = o;
    });
    return { model, joints };
  }, [scene, coat]);
  useFrame(({ clock }) => {
    const stride = reduced
      ? 0
      : Math.sin(clock.elapsedTime * 8) * motion.current.speed;
    if (joints.LeftLeg) joints.LeftLeg.rotation.x = stride * 0.48;
    if (joints.RightLeg) joints.RightLeg.rotation.x = -stride * 0.48;
    if (joints.LeftArm) joints.LeftArm.rotation.x = -stride * 0.36;
    if (joints.RightArm) joints.RightArm.rotation.x = stride * 0.36;
    if (joints.Head)
      joints.Head.rotation.y = reduced
        ? 0
        : Math.sin(clock.elapsedTime * 0.5) * 0.08;
  });
  return <primitive object={model} dispose={null} />;
};
