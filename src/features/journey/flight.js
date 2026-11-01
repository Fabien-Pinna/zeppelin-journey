/** Model nose is local +Z; keep the camera in its aft hemisphere. */
export function flightCameraOffset(heading, orbit = 0, portrait = false) {
  const angle = heading + Math.PI + Math.max(-1.05, Math.min(1.05, orbit));
  const distance = portrait ? 30 : 24;
  return [Math.sin(angle) * distance, portrait ? 11 : 9, Math.cos(angle) * distance];
}

/** Integrate engine spin smoothly; stopped simulation time freezes the rotors. */
export function stepPropellers(state, delta, flying, reduced = false) {
  const dt = Math.max(0, Math.min(delta, 0.05));
  const target = flying ? (reduced ? 2 : 18) : 0;
  state.speed += (target - state.speed) * (1 - Math.exp(-3 * dt));
  if (!flying && state.speed < 0.01) state.speed = 0;
  state.angle = (state.angle + state.speed * dt) % (Math.PI * 2);
  return state.angle;
}
