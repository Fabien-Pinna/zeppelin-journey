import test from 'node:test';
import assert from 'node:assert/strict';
import { flightCameraOffset, stepPropellers } from '../src/features/journey/flight.js';
import { readFileSync } from 'node:fs';

test('chase camera stays behind the model nose for every heading and orbit limit', () => {
  for (let yaw = -Math.PI; yaw <= Math.PI; yaw += 0.13) {
    for (const orbit of [-10, -1, 0, 1, 10]) {
      for (const portrait of [false, true]) {
        const [x, y, z] = flightCameraOffset(yaw, orbit, portrait);
        assert.ok(x * Math.sin(yaw) + z * Math.cos(yaw) < -10);
        assert.ok(y > 0);
      }
    }
  }
});

test('propellers spool up, freeze during pause and coast to rest after landing', () => {
  const state = { speed: 0, angle: 0 };
  for (let i = 0; i < 120; i++) stepPropellers(state, 1 / 60, true);
  assert.ok(state.speed > 17);
  const angle = state.angle;
  stepPropellers(state, 0, true);
  assert.equal(state.angle, angle);
  for (let i = 0; i < 240; i++) stepPropellers(state, 1 / 60, false);
  assert.equal(state.speed, 0);
  const stopped = state.angle;
  stepPropellers(state, 1 / 60, false);
  assert.equal(state.angle, stopped);
});

test('export preserves independently animated propeller and sheep meshes', () => {
  const read = (asset) => {
    const bytes = readFileSync(new URL(`../public/models/world-v2/${asset}.glb`, import.meta.url));
    return JSON.parse(bytes.toString('utf8', 20, 20 + bytes.readUInt32LE(12)));
  };
  for (const [asset, names] of [
    ['zeppelin', ['ANIM-propeller-L', 'ANIM-propeller-R']],
    ['farm', ['ANIM-sheep-a-head', 'ANIM-sheep-b-head', 'ANIM-sheep-a-leg-00', 'ANIM-sheep-b-leg-11']],
  ]) {
    const gltf = read(asset);
    for (const name of names) {
      const node = gltf.nodes.find((node) => node.name === name);
      assert.ok(node?.children?.length, `${asset}: ${name} has its own child geometry`);
      assert.ok(node.children.some((i) => gltf.nodes[i].mesh !== undefined));
    }
  }
});
