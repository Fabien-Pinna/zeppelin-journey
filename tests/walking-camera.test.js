import test from 'node:test';
import assert from 'node:assert/strict';
import { createWalkingFollow, stepWalkingFollow, walkingDirection, walkingCameraOffset, cameraObjectFraction } from '../src/features/journey/camera.js';
import * as THREE from 'three';

const error = (a, b) => Math.atan2(Math.sin(a - b), Math.cos(a - b));
const settle = (state, yaw, facing, version = 0, seconds = 5, rate = 60) => {
  for (let i = 0; i < seconds * rate; i++)
    yaw = stepWalkingFollow(state, yaw, facing, version, 0, 1 / rate);
  return yaw;
};

test('walking camera follows behind every character heading, including wrapped angles', () => {
  for (const facing of [-3.14, -2, -0.1, 0, 2, 3.14, 9]) {
    const yaw = settle(createWalkingFollow(), 0, facing);
    assert.ok(Math.abs(error(yaw, facing + Math.PI)) < 0.001);
    const [x, , z] = walkingCameraOffset(yaw);
    assert.ok(x * Math.sin(facing) + z * Math.cos(facing) < -13.9);
  }
  const yaw = stepWalkingFollow(createWalkingFollow(), Math.PI - 0.01, 0.01, 0, 0, 1 / 60);
  assert.ok(yaw > Math.PI - 0.01, 'crosses the seam by the short arc');
});

test('manual look holds for 1.2 seconds then returns even when the character is stationary', () => {
  const state = createWalkingFollow();
  let yaw = stepWalkingFollow(state, 1.5, Math.PI, 1, 0, 1 / 60);
  for (let i = 0; i < 60; i++) yaw = stepWalkingFollow(state, yaw, Math.PI, 1, 0, 1 / 60);
  assert.equal(yaw, 1.5);
  yaw = settle(state, yaw, Math.PI, 1);
  assert.ok(Math.abs(error(yaw, 0)) < 0.001);
});

test('ongoing look, including vertical-only input, restarts the idle delay; pause freezes it', () => {
  const state = createWalkingFollow();
  for (let version = 1; version < 240; version++) {
    assert.equal(stepWalkingFollow(state, 1.4, Math.PI, version, 0, 1 / 60), 1.4);
  }
  const before = { ...state };
  assert.equal(stepWalkingFollow(state, 1.4, 0, 999, 1, 0), 1.4);
  assert.deepEqual(state, before);
});

test('manual recenter targets the character back, independent of the world axes', () => {
  const state = createWalkingFollow();
  stepWalkingFollow(state, 0, 0.7, 1, 0, 1 / 60);
  const yaw = stepWalkingFollow(state, 0, 0.7, 1, 1, 1 / 60);
  assert.ok(Math.abs(error(yaw, 0.7 + Math.PI)) < 1e-10);
});

test('automatic following and free look never bend a held sideways or backward movement', () => {
  for (const [x, y] of [[1, 0], [-1, 0], [0, -1], [1, 1]]) {
    const state = createWalkingFollow();
    const direction = walkingDirection(state, x, y, 0);
    let yaw = 0;
    for (let frame = 0; frame < 360; frame++) {
      const next = walkingDirection(state, x, y, yaw);
      assert.deepEqual(next, direction);
      yaw = stepWalkingFollow(state, yaw, Math.atan2(next[0], next[1]), 0, 0, 1 / 60);
    }
    assert.deepEqual(walkingDirection(state, x, y, yaw + 1), direction);
    walkingDirection(state, 0, 0, yaw);
    const resumed = walkingDirection(state, 0, 1, yaw);
    assert.ok(Math.abs(resumed[0] + Math.sin(yaw)) < 1e-10);
    assert.ok(Math.abs(resumed[1] + Math.cos(yaw)) < 1e-10);
  }
});

test('follow damping is consistent across frame rates', () => {
  const results = [30, 60, 144].map((rate) => settle(createWalkingFollow(), 0.2, 1.1, 0, 1, rate));
  for (const result of results) assert.ok(Math.abs(result - results[0]) < 1e-10);
});

test('walking view stops before the parked ship, including transformed child geometry', () => {
  const ship = new THREE.Group();
  const envelope = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 12), new THREE.MeshBasicMaterial());
  envelope.scale.set(3, 2, 5);
  envelope.position.y = 3;
  ship.add(envelope);
  ship.position.set(8, -1, 2);
  ship.rotation.y = 0.4;
  const from = new THREE.Vector3(0, 2, 2);
  const to = new THREE.Vector3(15, 2, 2);
  const raycaster = new THREE.Raycaster();
  const hits = [];
  const fraction = cameraObjectFraction(from, to, ship, raycaster, hits);
  assert.ok(fraction > 0.2 && fraction < 0.4);
  assert.ok(Math.abs(hits[0].distance - from.distanceTo(to) * fraction - 0.4) < 1e-9);
  assert.equal(cameraObjectFraction(from, new THREE.Vector3(-10, 2, 2), ship, raycaster, hits), 1);
  envelope.geometry.dispose();
  envelope.material.dispose();
});
