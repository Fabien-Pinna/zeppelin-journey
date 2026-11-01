// Preserve the original walking view: 14 m back, 6.7 m above the look target.
export const DEFAULT_WALK_PITCH = Math.atan2(6.7, 14);
const WALK_DISTANCE = Math.hypot(14, 6.7);
export const WALK_LOOK_DELAY = 1.2;

const angleDifference = (target, current) => Math.atan2(Math.sin(target - current), Math.cos(target - current));

/** Start aligned behind the traveller, ready to follow its next turn. */
export const createWalkingFollow = (lookVersion = 0, recenterVersion = 0) => ({
  idle: WALK_LOOK_DELAY,
  lookVersion,
  recenterVersion,
  movementHeading: 0,
  moving: false,
});

/** Keep a held movement gesture stable while the camera follows or looks around. */
export function walkingDirection(state, x, y, cameraYaw) {
  const magnitude = Math.hypot(x, y);
  if (magnitude <= 0.05) {
    state.moving = false;
    return [0, 0];
  }
  if (!state.moving) state.movementHeading = cameraYaw;
  state.moving = true;
  const angle = state.movementHeading;
  const length = Math.max(1, magnitude);
  return [
    (x * Math.cos(angle) - y * Math.sin(angle)) / length,
    (-y * Math.cos(angle) - x * Math.sin(angle)) / length,
  ];
}

/** Yield to real look input, then return behind +Z-facing anatomy via the shortest arc. */
export function stepWalkingFollow(state, yaw, facing, lookVersion, recenterVersion, delta) {
  const dt = Math.max(0, Math.min(delta, 0.05));
  if (!dt) return yaw;
  const target = facing + Math.PI;
  if (recenterVersion !== state.recenterVersion) {
    state.recenterVersion = recenterVersion;
    state.lookVersion = lookVersion;
    state.idle = WALK_LOOK_DELAY;
    return yaw + angleDifference(target, yaw);
  }
  if (lookVersion !== state.lookVersion) {
    state.lookVersion = lookVersion;
    state.idle = 0;
    return yaw;
  }
  state.idle += dt;
  if (state.idle <= WALK_LOOK_DELAY) return yaw;
  return yaw + angleDifference(target, yaw) * (1 - Math.exp(-2.4 * dt));
}

export const clampWalkPitch = (pitch) => Math.max(0.06, Math.min(1.35, pitch));

/** Stop before visible ship geometry, which is absent from the island collider manifest. */
export function cameraObjectFraction(from, to, object, raycaster, hits) {
  raycaster.ray.origin.copy(from);
  raycaster.ray.direction.copy(to).sub(from);
  const distance = raycaster.ray.direction.length();
  if (distance < 0.001) return 1;
  raycaster.ray.direction.normalize();
  raycaster.near = 0;
  raycaster.far = distance + 0.4;
  hits.length = 0;
  object.updateWorldMatrix(true, true);
  raycaster.intersectObject(object, true, hits);
  return hits.length ? Math.min(1, Math.max(0.08, (hits[0].distance - 0.4) / distance)) : 1;
}

/** Orbit at a constant distance; zoom and obstacle avoidance are applied afterwards. */
export function walkingCameraOffset(heading, pitch = DEFAULT_WALK_PITCH) {
  const elevation = clampWalkPitch(pitch);
  const horizontal = WALK_DISTANCE * Math.cos(elevation);
  return [
    Math.sin(heading) * horizontal,
    WALK_DISTANCE * Math.sin(elevation),
    Math.cos(heading) * horizontal,
  ];
}
