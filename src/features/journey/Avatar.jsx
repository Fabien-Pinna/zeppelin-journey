import { assetUrl } from "../../assetUrl.js";
import { useMemo } from "react";
import { useGLTF } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { JOINTS, jointName } from "./joints.js";
/** Original Blender-authored character, with independent runtime joints. */
export const Avatar = ({
  motion,
  reduced,
  coat,
  pose = "walk",
  simulation,
}) => {
  const { scene } = useGLTF(
    assetUrl(`models/world-v2/${pose === "hang" || pose === "juggle" ? "acrobat" : "traveller"}.glb`),
  );
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
      const name = jointName(o.name);
      if (name) joints[name] = o;
    });
    if (JOINTS.some((name) => !joints[name]))
      throw new Error("Le personnage ne possède pas toutes ses articulations.");
    return { model, joints };
  }, [scene, coat]);
  useFrame(({ clock }) => {
    const time = simulation ? simulation.current.time : clock.elapsedTime;
    const stride = reduced
      ? 0
      : Math.sin(time * 8) * (motion?.current.speed || 0);
    if (joints.LeftLeg) joints.LeftLeg.rotation.x = stride * 0.48;
    if (joints.RightLeg) joints.RightLeg.rotation.x = -stride * 0.48;
    if (joints.LeftArm) joints.LeftArm.rotation.x = -stride * 0.36;
    if (joints.RightArm) joints.RightArm.rotation.x = stride * 0.36;
    if (joints.Head)
      joints.Head.rotation.y = reduced ? 0 : Math.sin(time * 0.5) * 0.08;
    if (pose === "hang") {
      for (const name of ["LeftArm", "RightArm"]) {
        joints[name].rotation.x = Math.PI;
        joints[name].position.y = 1.64;
      }
      joints.LeftLeg.rotation.x = Math.sin(time * 1.8) * 0.18;
      joints.RightLeg.rotation.x = Math.sin(time * 1.8 + 0.4) * 0.18;
    } else if (pose === "carry" || pose === "read") {
      joints.LeftArm.rotation.x = -0.92;
      joints.RightArm.rotation.x =
        -0.92 + (pose === "read" ? Math.sin(time * 1.3) * 0.07 : 0);
      joints.Head.rotation.x = pose === "read" ? 0.18 : 0;
    } else if (pose === "hammer" || pose === "repair") {
      joints.RightArm.rotation.x =
        -0.85 + Math.sin(time * (pose === "hammer" ? 4 : 2)) * 0.42;
      joints.LeftArm.rotation.x = -0.6;
      joints.Head.rotation.x = 0.12;
    } else if (pose === "teach" || pose === "create") {
      joints.RightArm.rotation.x = -1.5 + Math.sin(time * 1.2) * 0.18;
      joints.LeftArm.rotation.x = -0.4;
    } else if (pose === "garden") {
      joints.RightArm.rotation.x = -0.8 + Math.sin(time * 1.5) * 0.1;
      joints.LeftArm.rotation.x = -0.3;
      joints.Head.rotation.x = 0.1;
    } else if (pose === "juggle") {
      joints.LeftArm.rotation.x = -0.8 + Math.sin(time * 4.4) * 0.28;
      joints.RightArm.rotation.x = -0.8 - Math.sin(time * 4.4) * 0.28;
    } else if (pose === "greet") {
      joints.RightArm.rotation.x = -0.25 + Math.sin(time * 0.8) * 0.18;
    }
  });
  return <primitive object={model} dispose={null} />;
};
