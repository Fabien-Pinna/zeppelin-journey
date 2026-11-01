import { activityPosition } from "./activities.js";
import layouts from "./layouts.json" with { type: "json" };
import { islandBoundary } from './landscape.js';

export const BODY_RADIUS = 0.32;
export const BODY_HEIGHT = 2.25;
export const GUIDE_POSITION = [3.8, 0.02, 5.9];
export const clampZoom = (value) => Math.max(0.55, Math.min(1.8, value));

// The collider manifest is exported alongside the visible Blender geometry.
export const obstaclesFor = (id, time = 0) => [
  ...(layouts[id] || []),
  {
    name: "guide",
    type: "cylinder",
    position: GUIDE_POSITION,
    size: [0.65, 4, 0.65],
  },
  ...(activityPosition(id, time)
    ? [
        {
          name: "worker",
          type: "cylinder",
          position: [
            activityPosition(id, time)[0],
            1,
            activityPosition(id, time)[2],
          ],
          size: [0.6, 2, 0.6],
        },
      ]
    : []),
  ...(id === "farm"
    ? [
        {
          name: "sheep-a",
          type: "box",
          position: [2.12 + Math.sin(time * 0.35) * 0.35, 0.65, 2],
          size: [1.75, 1.3, 0.86],
        },
        {
          name: "sheep-b",
          type: "box",
          position: [3.9, 0.52, 3 + Math.sin(time * 0.3) * 0.25],
          size: [1.4, 1.04, 0.72],
        },
      ]
    : []),
  ...(id === 'circus' ? [
    { name: 'stage-manager', type: 'cylinder', position: [-6,1,4.5], size: [.65,2,.65] },
    { name: 'clown', type: 'cylinder', position: [5,1,.8], size: [.65,2,.65] },
  ] : []),
];

export function penetration(x, z, obstacle, radius = BODY_RADIUS) {
  const [ox, , oz] = obstacle.position;
  const [width, , depth] = obstacle.size;
  if (obstacle.type === "cylinder") {
    const dx = x - ox,
      dz = z - oz,
      distance = Math.hypot(dx, dz);
    const overlap = radius + width / 2 - distance;
    return overlap > 0
      ? [
          distance ? (dx / distance) * overlap : overlap,
          distance ? (dz / distance) * overlap : 0,
        ]
      : null;
  }
  const left = ox - width / 2,
    right = ox + width / 2;
  const back = oz - depth / 2,
    front = oz + depth / 2;
  const cx = Math.max(left, Math.min(right, x)),
    cz = Math.max(back, Math.min(front, z));
  const dx = x - cx,
    dz = z - cz,
    distance = Math.hypot(dx, dz);
  if (distance >= radius) return null;
  if (distance > 0.000001)
    return [
      (dx / distance) * (radius - distance),
      (dz / distance) * (radius - distance),
    ];
  const exits = [
    [left - radius - x, 0],
    [right + radius - x, 0],
    [0, back - radius - z],
    [0, front + radius - z],
  ];
  return exits.sort((a, b) => Math.hypot(...a) - Math.hypot(...b))[0];
}

/** Substeps prevent tunnelling; projection preserves movement along walls. */
export function moveWalker(x, z, dx, dz, island, feet = 0.02, time = 0) {
  let lx = x - island.position[0],
    lz = z - island.position[2];
  const obstacles = obstaclesFor(island.id, time).filter(
    (o) =>
      feet + BODY_HEIGHT > o.position[1] - o.size[1] / 2 + 0.04 &&
      feet < o.position[1] + o.size[1] / 2 - 0.03,
  );
  const steps = Math.max(1, Math.ceil(Math.hypot(dx, dz) / 0.12));
  for (let step = 0; step < steps; step++) {
    lx += dx / steps;
    lz += dz / steps;
    for (let pass = 0; pass < 4; pass++) {
      for (const obstacle of obstacles) {
        const push = penetration(lx, lz, obstacle);
        if (push) {
          lx += push[0];
          lz += push[1];
        }
      }
      const distance = Math.hypot(lx, lz),
        limit = islandBoundary(island.id, Math.atan2(lz, lx)) - 0.9;
      if (distance > limit) {
        lx *= limit / distance;
        lz *= limit / distance;
      }
    }
  }
  return [lx + island.position[0], lz + island.position[2]];
}

export function groundHeight(x, z, island) {
  const lx = x - island.position[0],
    lz = z - island.position[2];
  if (lx > 4.8 && lx < 9.2 && lz > 2.5 && lz < 9.8) return 0.2;
  if (island.id === "atelier" && lx > -6 && lx < 2 && lz > -6 && lz < 0)
    return 0.25;
  return 0.02;
}

/** Keep the camera on the player's side of solid walls and tall furniture. */
export function cameraFraction(from, to, island) {
  let fraction = 1;
  for (const o of layouts[island.id] || []) {
    if (
      o.size[1] < 1.4 ||
      ["tree", "lantern", "bunting-post", "pier-post"].includes(o.name)
    )
      continue;
    let enter = 0,
      leave = 1;
    for (let axis = 0; axis < 3; axis++) {
      const center = o.position[axis] + island.position[axis];
      const half = o.size[axis] / 2 + 0.15;
      const direction = to[axis] - from[axis];
      if (Math.abs(direction) < 0.00001) {
        if (from[axis] < center - half || from[axis] > center + half) {
          enter = 2;
          break;
        }
      } else {
        const a = (center - half - from[axis]) / direction;
        const b = (center + half - from[axis]) / direction;
        enter = Math.max(enter, Math.min(a, b));
        leave = Math.min(leave, Math.max(a, b));
      }
    }
    if (enter <= leave && enter > 0.08)
      fraction = Math.min(fraction, Math.max(0.08, enter - 0.025));
  }
  return fraction;
}

export const TRAPEZE = {
  length: 2.96,
  pivot: [-4.3, 6.856, 0.088],
  gripHeight: 2.33,
  scale: 0.7,
  net: { height: 2.032, back: -9.32, front: 5.72 },
};
export const createPendulum = () => ({
  angle: 0.58,
  velocity: 0,
  accumulator: 0,
});
/** Fixed-step, gently driven physical pendulum. Gravity sets its period. */
export function stepPendulum(state, delta) {
  const h = 1 / 120;
  state.accumulator += Math.min(delta, 0.05);
  while (state.accumulator >= h) {
    const drive = 0.055 * state.velocity * (1 - (state.angle / 0.36) ** 2);
    state.velocity +=
      ((-9.81 / TRAPEZE.length) * Math.sin(state.angle) -
        0.018 * state.velocity +
        drive) *
      h;
    state.angle += state.velocity * h;
    state.accumulator -= h;
  }
  return state.angle;
}
export function trapezePoint(angle, local) {
  return [
    TRAPEZE.pivot[0] + local[0],
    TRAPEZE.pivot[1] + local[1] * Math.cos(angle) - local[2] * Math.sin(angle),
    TRAPEZE.pivot[2] + local[1] * Math.sin(angle) + local[2] * Math.cos(angle),
  ];
}
export function jugglingBall(time, index) {
  const cycle = (time * 0.7 + (index * 2) / 3) % 2;
  const phase = cycle % 1,
    side = cycle < 1 ? -1 : 1;
  return [
    side * (0.42 - 0.84 * phase),
    1.28 + 6.8 * phase * (1 - phase),
    0.3 + side * 0.22 * Math.sin(Math.PI * phase),
  ];
}
