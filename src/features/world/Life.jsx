import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import { Html } from "@react-three/drei";
import { Avatar } from "../journey/Avatar.jsx";
import { GUIDE_POSITION, TRAPEZE, jugglingBall } from "../journey/physics.js";
import { activities, activityPosition } from "../journey/activities.js";
import { conversations } from "../journey/conversations.js";

const Prop = ({ position, scale, color = "#bb925f", ...props }) => (
  <mesh position={position} scale={scale} castShadow {...props}>
    <boxGeometry />
    <meshStandardMaterial color={color} roughness={0.72} />
  </mesh>
);

export function Guide({ island, simulation, onTalk }) {
  const ref = useRef();
  useFrame(() => {
    if (!ref.current) return;
    const player = simulation.current.player;
    const dx = player[0] - island.position[0] - GUIDE_POSITION[0];
    const dz = player[2] - island.position[2] - GUIDE_POSITION[2];
    ref.current.rotation.y = Math.hypot(dx, dz) < 7 ? Math.atan2(dx, dz) : -0.4;
  });
  return (
    <group position={GUIDE_POSITION}>
      <group
        ref={ref}
        onClick={(e) => {
          e.stopPropagation();
          onTalk(island.id);
        }}
      >
        <Avatar pose="greet" simulation={simulation} coat={island.color} />
      </group>
      <Html
        position={[0, 2.85, 0]}
        center
        distanceFactor={15}
        zIndexRange={[12, 1]}
      >
        <button
          className="npc-label"
          onPointerDown={(e) => e.stopPropagation()}
          onClick={() => onTalk(island.id)}
        >
          <span>•••</span> {conversations[island.id].name}
        </button>
      </Html>
    </group>
  );
}

export function Trapeze({ simulation }) {
  const pivot = useRef();
  useFrame(() => {
    pivot.current.rotation.x = simulation.current.pendulum.angle;
  });
  return (
    <group position={TRAPEZE.pivot} ref={pivot}>
      {[-0.36, 0.36].map((x) => (
        <mesh key={x} position={[x, -TRAPEZE.length / 2, 0]} castShadow>
          <cylinderGeometry args={[0.022, 0.022, TRAPEZE.length, 8]} />
          <meshStandardMaterial color="#c5ab77" />
        </mesh>
      ))}
      <mesh
        position={[0, -TRAPEZE.length, 0]}
        rotation={[0, 0, Math.PI / 2]}
        castShadow
      >
        <cylinderGeometry args={[0.045, 0.045, 1.3, 12]} />
        <meshStandardMaterial color="#9a6e3e" />
      </mesh>
      <group
        position={[
          0,
          -TRAPEZE.length - TRAPEZE.gripHeight * TRAPEZE.scale,
          0.02 * TRAPEZE.scale,
        ]}
        scale={TRAPEZE.scale}
      >
        <Avatar pose="hang" coat="#bd634a" simulation={simulation} />
      </group>
    </group>
  );
}

export function Activity({ id, simulation }) {
  const actor = useRef(),
    balls = useRef([]),
    page = useRef(),
    tool = useRef();
  const motion = useRef({ speed: 0 });
  const setup = activities[id];
  useFrame(() => {
    const t = simulation.current.time;
    if (id === "warehouse") {
      actor.current.position.set(...activityPosition(id, t));
      actor.current.rotation.y =
        (Math.PI / 2) * Math.tanh(Math.cos(t * 0.42) * 8);
      motion.current.speed = Math.abs(Math.cos(t * 0.42)) * 0.45;
    }
    if (id === "circus")
      balls.current.forEach((ball, index) =>
        ball.position.set(...jugglingBall(t, index)),
      );
    if (page.current)
      page.current.rotation.z = -0.15 + Math.sin(t * 0.8) * 0.18;
    if (tool.current) {
      // Match the right hand transform of the rigid arm, including its pivot.
      const angle = -0.85 + Math.sin(t * (id === "masonry" ? 4 : 2)) * 0.42;
      tool.current.position.set(
        0.4,
        1.52 - 0.69 * Math.cos(angle) - 0.02 * Math.sin(angle),
        -0.69 * Math.sin(angle) + 0.02 * Math.cos(angle),
      );
      tool.current.rotation.x = angle;
    }
  });
  if (id === "clubmed") return <Trapeze simulation={simulation} />;
  return (
    <group ref={actor} position={setup.position} rotation-y={setup.rotation}>
      <Avatar
        pose={setup.pose}
        motion={motion}
        simulation={simulation}
        coat={setup.color}
      />
      {id === "warehouse" && (
        <group position={[0, 1.08, 0.69]}>
          <Prop scale={[0.8, 0.55, 0.55]} />
          <Prop
            scale={[0.86, 0.08, 0.58]}
            position={[0, 0.18, 0]}
            color="#755137"
          />
          <Prop
            scale={[0.86, 0.08, 0.58]}
            position={[0, -0.18, 0]}
            color="#755137"
          />
        </group>
      )}
      {(id === "masonry" || id === "backroads") && (
        <group ref={tool}>
          <Prop
            position={[0, 0, 0.12]}
            scale={[0.045, 0.045, 0.35]}
            color="#79532e"
          />
          <Prop
            position={[0, 0, 0.3]}
            scale={id === "masonry" ? [0.22, 0.1, 0.12] : [0.13, 0.04, 0.15]}
            color="#69716a"
          />
        </group>
      )}
      {id === "farm" && (
        <group position={[0.5, 1, 0.6]}>
          <mesh castShadow>
            <cylinderGeometry args={[0.15, 0.17, 0.3, 12]} />
            <meshStandardMaterial
              color="#8dada2"
              metalness={0.35}
              roughness={0.4}
            />
          </mesh>
          <Prop
            position={[0, -0.02, 0.2]}
            scale={[0.06, 0.06, 0.35]}
            color="#8dada2"
          />
        </group>
      )}
      {id === "learning" && (
        <group position={[0, 1.16, 0.65]} rotation-x={-0.2}>
          <Prop scale={[0.8, 0.04, 0.45]} color="#7c4e36" />
          <Prop
            scale={[0.76, 0.03, 0.42]}
            position={[0, 0.035, 0]}
            color="#e7d8ad"
          />
          <group ref={page}>
            <Prop
              position={[0.18, 0.055, 0]}
              scale={[0.35, 0.012, 0.4]}
              color="#f5e7c5"
            />
          </group>
        </group>
      )}
      {id === "circus" &&
        ["#cf9250", "#538c8a", "#b85147"].map((color, index) => (
          <mesh
            key={color}
            ref={(el) => {
              balls.current[index] = el;
            }}
            castShadow
          >
            <sphereGeometry args={[0.105, 16, 12]} />
            <meshStandardMaterial color={color} roughness={0.4} />
          </mesh>
        ))}
    </group>
  );
}

/** Animate the named glTF pivots; no full-scene React renders per frame. */
export function useScenicMotion(model, simulation) {
  const nodes = useMemo(() => {
    const found = {};
    model.traverse((node) => {
      if (node.name.startsWith("ANIM-"))
        found[node.name] = {
          node,
          position: node.position.clone(),
          rotation: node.rotation.clone(),
        };
    });
    return found;
  }, [model]);
  useFrame(() => {
    const t = simulation.current.time;
    for (const [name, { node, position, rotation }] of Object.entries(nodes)) {
      if (name === "ANIM-windmill") node.rotation.z = rotation.z - t * 0.3;
      if (name === "ANIM-clock-minute") node.rotation.z = rotation.z - t * 0.08;
      if (name === "ANIM-clock-hour")
        node.rotation.z = rotation.z - (t * 0.08) / 12;
      if (name === "ANIM-sheep-a") {
        node.position.x = position.x + Math.sin(t * 0.35) * 0.35;
        node.rotation.y = rotation.y + Math.sin(t * 0.5) * 0.09;
      }
      if (name === "ANIM-sheep-b") {
        node.position.z = position.z + Math.sin(t * 0.3) * 0.25;
        node.rotation.y = rotation.y + Math.sin(t * 0.4) * 0.12;
      }
    }
  });
}
