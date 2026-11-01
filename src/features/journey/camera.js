// Preserve the original walking view: 14 m back, 6.7 m above the look target.
export const DEFAULT_WALK_PITCH = Math.atan2(6.7, 14);
const WALK_DISTANCE = Math.hypot(14, 6.7);

export const clampWalkPitch = (pitch) => Math.max(0.06, Math.min(1.35, pitch));

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
