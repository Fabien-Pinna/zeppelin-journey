import { useMemo } from 'react';
import { useGLTF } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';
import { clone } from 'three/examples/jsm/utils/SkeletonUtils.js';
import * as THREE from 'three';

/** Animate the supplied Ready Player Me rig without altering its cached source. */
export const Avatar = ({ motion, reduced }) => {
  const { scene } = useGLTF('/models/fabien.glb');
  const { model, bones } = useMemo(() => {
    const model = clone(scene);
    const bones = {};
    model.traverse(object => {
      if (object.isMesh) { object.castShadow = true; object.frustumCulled = false; }
      if (object.isBone) bones[object.name] = { object, rest: object.quaternion.clone() };
    });
    model.updateMatrixWorld(true);
    for (const [name, side] of [['LeftArm', 1], ['RightArm', -1]]) {
      const bone = bones[name];
      if (!bone) continue;
      const worldRotation = bone.object.getWorldQuaternion(new THREE.Quaternion());
      const parentRotation = bone.object.parent.getWorldQuaternion(new THREE.Quaternion());
      const currentDirection = new THREE.Vector3(0, 1, 0).applyQuaternion(worldRotation);
      const relaxedDirection = new THREE.Vector3(side * 0.12, -1, 0).normalize();
      const correction = new THREE.Quaternion().setFromUnitVectors(currentDirection, relaxedDirection);
      bone.rest.copy(parentRotation.invert().multiply(correction.multiply(worldRotation)));
    }
    return { model, bones };
  }, [scene]);
  const q = useMemo(() => new THREE.Quaternion(), []);
  const axis = useMemo(() => new THREE.Vector3(), []);
  useFrame(({ clock }) => {
    const stride = reduced ? 0 : Math.sin(clock.elapsedTime * 9) * motion.current.speed;
    const rotate = (name, x, z = 0) => {
      const bone = bones[name];
      if (!bone) return;
      bone.object.quaternion.copy(bone.rest);
      q.setFromAxisAngle(axis.set(0, 0, 1), z); bone.object.quaternion.multiply(q);
      q.setFromAxisAngle(axis.set(1, 0, 0), x); bone.object.quaternion.multiply(q);
    };
    rotate('LeftArm', stride * 0.25);
    rotate('RightArm', -stride * 0.25);
    rotate('LeftUpLeg', stride * 0.45); rotate('RightUpLeg', -stride * 0.45);
    rotate('LeftLeg', Math.max(0, -stride) * 0.4); rotate('RightLeg', Math.max(0, stride) * 0.4);
  });
  return <primitive object={model} dispose={null} />;
};
