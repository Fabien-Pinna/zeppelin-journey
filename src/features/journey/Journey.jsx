import { Suspense, useEffect, useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { Avatar } from "./Avatar.jsx";
import { Zeppelin } from "../world/Zeppelin.jsx";
import {
  moveWalker,
  deadZone,
  dockPosition,
  berthPosition,
  islands,
  nearestIsland,
} from "./world.js";

import {
  groundHeight,
  GUIDE_POSITION,
  clampZoom,
  cameraFraction,
} from "./physics.js";

/** Frame-driven movement, flight and assisted docking with a damped camera. */
export const Journey = ({
  mode,
  setMode,
  islandId,
  setIslandId,
  destination,
  setDestination,
  input,
  actionRef,
  telemetry,
  reduced,
  paused,
  simulation,
}) => {
  const avatar = useRef(),
    ship = useRef();
  const walker = useRef(new THREE.Vector3(7, 0.2, 8));
  const vessel = useRef(new THREE.Vector3(...berthPosition(islands[0])));
  const motion = useRef({ speed: 0 });
  const vertical = useRef({ velocity: 0, jumpHeld: false });
  const heading = useRef(0),
    timer = useRef(0),
    gamepadAction = useRef(false);
  const vectors = useMemo(
    () => ({
      camera: new THREE.Vector3(),
      look: new THREE.Vector3(),
      smoothLook: new THREE.Vector3(-6, 2, -13),
      target: new THREE.Vector3(),
      forward: new THREE.Vector3(),
    }),
    [],
  );
  const island = islands.find((item) => item.id === islandId);
  useEffect(() => {
    actionRef.current = () => {
      if (paused) return;
      if (mode === "walking") {
        const dock = dockPosition(island);
        if (
          Math.hypot(walker.current.x - dock[0], walker.current.z - dock[2]) <
          4.5
        )
          setMode("takeoff");
      } else if (mode === "flying") {
        const near = nearestIsland(vessel.current.x, vessel.current.z);
        if (near.distance < 18) {
          setIslandId(near.island.id);
          setDestination(near.island.id);
          setMode("landing");
        }
      }
    };
  }, [mode, island, paused, setMode, setIslandId, setDestination, actionRef]);

  useFrame(({ camera }, rawDelta) => {
    const dt = Math.min(rawDelta, 0.05);
    const { keys, touch } = input.current;
    const pad = navigator.getGamepads?.()?.find((p) => p?.connected);
    const has = (...codes) => codes.some((code) => keys.has(code));
    let x =
      Number(has("KeyD", "ArrowRight")) -
      Number(has("KeyA", "KeyQ", "ArrowLeft")) +
      touch.x +
      deadZone(pad?.axes[0] || 0);
    let y =
      Number(has("KeyW", "KeyZ", "ArrowUp")) -
      Number(has("KeyS", "ArrowDown")) -
      touch.y -
      deadZone(pad?.axes[1] || 0);
    x = THREE.MathUtils.clamp(x, -1, 1);
    y = THREE.MathUtils.clamp(y, -1, 1);
    const action = pad?.buttons[0]?.pressed || false;
    if (action && !gamepadAction.current && !paused) actionRef.current?.();
    gamepadAction.current = action;
    if (!paused) input.current.orbit += deadZone(pad?.axes[2] || 0) * dt * 1.5;
    if (paused) {
      x = 0;
      y = 0;
    }

    if (mode === "walking" && !paused) {
      const angle = input.current.orbit;
      const length = Math.max(1, Math.hypot(x, y));
      const dx = (x * Math.cos(angle) - y * Math.sin(angle)) / length;
      const dz = (-y * Math.cos(angle) - x * Math.sin(angle)) / length;
      const speed = has("ShiftLeft", "ShiftRight") ? 5.6 : 3.2;
      const feet = walker.current.y - island.position[1];
      const [nx, nz] = moveWalker(
        walker.current.x,
        walker.current.z,
        dx * speed * dt,
        dz * speed * dt,
        island,
        feet,
        simulation.current.time,
      );
      const floor = island.position[1] + groundHeight(nx, nz, island);
      const jump = has("Space") || input.current.jump;
      if (
        jump &&
        !vertical.current.jumpHeld &&
        walker.current.y <= floor + 0.035
      )
        vertical.current.velocity = 4.2;
      vertical.current.jumpHeld = jump;
      vertical.current.velocity -= 12 * dt;
      const height = Math.max(
        floor,
        walker.current.y + vertical.current.velocity * dt,
      );
      if (height === floor) vertical.current.velocity = 0;
      walker.current.set(nx, height, nz);
      motion.current.speed = THREE.MathUtils.damp(
        motion.current.speed,
        Math.min(1, Math.hypot(x, y)),
        9,
        dt,
      );
      if (Math.hypot(x, y) > 0.05) {
        const target = Math.atan2(dx, dz);
        avatar.current.rotation.y +=
          Math.atan2(
            Math.sin(target - avatar.current.rotation.y),
            Math.cos(target - avatar.current.rotation.y),
          ) *
          (1 - Math.exp(-12 * dt));
      }
    } else motion.current.speed = 0;

    if (mode === "takeoff" && !paused) {
      vessel.current.y = THREE.MathUtils.damp(
        vessel.current.y,
        island.position[1] + 18,
        1.5,
        dt,
      );
      if (vessel.current.y > island.position[1] + 17.5) setMode("flying");
    }
    if (mode === "flying" && !paused) {
      if (destination) {
        const targetIsland = islands.find((item) => item.id === destination);
        const dock = berthPosition(targetIsland);
        vectors.target.set(dock[0], targetIsland.position[1] + 18, dock[2]);
        vectors.forward.copy(vectors.target).sub(vessel.current);
        const distance = vectors.forward.length();
        heading.current = Math.atan2(vectors.forward.x, vectors.forward.z);
        vessel.current.addScaledVector(
          vectors.forward.normalize(),
          Math.min(distance, dt * 13),
        );
        if (distance < 0.6) {
          setIslandId(destination);
          setMode("landing");
        }
      } else {
        heading.current -= x * dt * 1.25;
        vessel.current.x += Math.sin(heading.current) * y * dt * 12;
        vessel.current.z += Math.cos(heading.current) * y * dt * 12;
        vessel.current.y +=
          (Number(Boolean(has("Space") || pad?.buttons[7]?.pressed)) -
            Number(
              Boolean(
                has("ShiftLeft", "ShiftRight") || pad?.buttons[6]?.pressed,
              ),
            )) *
          dt *
          6;
        vessel.current.x = THREE.MathUtils.clamp(vessel.current.x, -80, 80);
        vessel.current.z = THREE.MathUtils.clamp(vessel.current.z, -110, 55);
        vessel.current.y = THREE.MathUtils.clamp(vessel.current.y, 16, 35);
      }
    }
    if (mode === "landing" && !paused) {
      const dock = dockPosition(island),
        berth = berthPosition(island);
      heading.current = 0;
      vectors.target.set(...berth);
      vessel.current.lerp(vectors.target, 1 - Math.exp(-1.6 * dt));
      if (vessel.current.distanceTo(vectors.target) < 0.15) {
        vessel.current.copy(vectors.target);
        walker.current.set(dock[0] - 1, dock[1] + 0.2, dock[2] + 1);
        setDestination(null);
        setMode("walking");
      }
    }
    simulation.current.player = [
      walker.current.x,
      walker.current.y,
      walker.current.z,
    ];
    avatar.current.position.copy(walker.current);
    avatar.current.visible = mode === "walking" || mode === "overview";
    ship.current.position.copy(vessel.current);
    ship.current.rotation.y +=
      Math.atan2(
        Math.sin(heading.current - ship.current.rotation.y),
        Math.cos(heading.current - ship.current.rotation.y),
      ) *
      (1 - Math.exp(-3 * dt));

    if (mode === "overview") {
      vectors.camera.set(
        camera.aspect < 1 ? 35 : 24,
        camera.aspect < 1 ? 31 : 20,
        camera.aspect < 1 ? 58 : 36,
      );
      vectors.look.set(
        camera.aspect < 1 ? 5 : -6,
        2,
        camera.aspect < 1 ? 0 : -13,
      );
    } else if (mode === "landing") {
      const dock = dockPosition(island),
        angle = input.current.orbit;
      vectors.camera.set(
        dock[0] - 1 + Math.sin(angle) * 14,
        dock[1] + 8.2,
        dock[2] + 1 + Math.cos(angle) * 14,
      );
      vectors.look.set(dock[0] - 1, dock[1] + 1.5, dock[2] + 1);
    } else if (mode === "walking") {
      const angle = input.current.orbit;
      vectors.camera.set(
        walker.current.x + Math.sin(angle) * 14,
        walker.current.y + 8,
        walker.current.z + Math.cos(angle) * 14,
      );
      vectors.look.copy(walker.current).add(vectors.target.set(0, 1.3, 0));
    } else {
      const angle = ship.current.rotation.y + Math.PI + input.current.orbit;
      vectors.camera.set(
        vessel.current.x + Math.sin(angle) * 24,
        vessel.current.y + 12,
        vessel.current.z + Math.cos(angle) * 24,
      );
      vectors.look.copy(vessel.current).add(vectors.target.set(0, 2.8, 0));
    }
    const zoom = clampZoom(input.current.zoom);
    vectors.camera.sub(vectors.look).multiplyScalar(zoom).add(vectors.look);
    if (mode === "walking") {
      const fraction = cameraFraction(
        vectors.look.toArray(),
        vectors.camera.toArray(),
        island,
      );
      vectors.camera
        .sub(vectors.look)
        .multiplyScalar(fraction)
        .add(vectors.look);
    }
    camera.position.lerp(vectors.camera, reduced ? 1 : 1 - Math.exp(-3 * dt));
    vectors.smoothLook.lerp(vectors.look, reduced ? 1 : 1 - Math.exp(-5 * dt));
    camera.lookAt(vectors.smoothLook);
    timer.current += dt;
    if (timer.current > 0.15) {
      timer.current = 0;
      const near = nearestIsland(vessel.current.x, vessel.current.z),
        dock = dockPosition(island);
      telemetry({
        x: mode === "walking" ? walker.current.x : vessel.current.x,
        z: mode === "walking" ? walker.current.z : vessel.current.z,
        altitude: Math.round(vessel.current.y),
        near: near.island.id,
        canBoard:
          Math.hypot(walker.current.x - dock[0], walker.current.z - dock[2]) <
          4.5,
        canLand: near.distance < 18,
        gamepad: Boolean(pad),
        canTalk:
          mode === "walking" &&
          Math.hypot(
            walker.current.x - island.position[0] - GUIDE_POSITION[0],
            walker.current.z - island.position[2] - GUIDE_POSITION[2],
          ) < 3.4,
      });
    }
  });
  return (
    <>
      <group ref={avatar}>
        <Suspense fallback={null}>
          <Avatar
            motion={motion}
            reduced={reduced || paused}
            simulation={simulation}
          />
        </Suspense>
      </group>
      <group ref={ship}>
        <Zeppelin
          flying={mode !== "walking" && mode !== "overview"}
          reduced={reduced}
          simulation={simulation}
        />
      </group>
    </>
  );
};
