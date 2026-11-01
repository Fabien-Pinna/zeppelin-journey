import test from "node:test";
import assert from "node:assert/strict";
import {
  islands,
  constrainWalker,
  dockPosition,
  nearestIsland,
  deadZone,
} from "../src/features/journey/world.js";

test("each harbour is reachable on foot and selected by assisted docking", () => {
  for (const island of islands) {
    const [x, , z] = dockPosition(island);
    assert.deepEqual(constrainWalker(x, z, island), [x, z]);
    assert.equal(nearestIsland(x, z).island.id, island.id);
  }
});

test("walking cannot leave an island, even after a large input step", () => {
  for (const island of islands) {
    for (let a = 0; a < Math.PI * 2; a += 0.15) {
      const [x, z] = constrainWalker(
        island.position[0] + Math.cos(a) * 200,
        island.position[2] + Math.sin(a) * 200,
        island,
      );
      assert.ok(
        Math.hypot(x - island.position[0], z - island.position[2]) <=
          island.radius - 0.89,
      );
    }
  }
});

test("walking into the workshop resolves outside its walls", () => {
  const [x, z] = constrainWalker(-3, -3, islands[0]);
  assert.ok(Math.hypot(x + 3, z + 3) >= 3.39);
});

test("gamepad drift is ignored while full stick travel remains available", () => {
  assert.equal(deadZone(0.1), 0);
  assert.equal(deadZone(-0.1), 0);
  assert.equal(deadZone(1), 1);
  assert.equal(deadZone(-1), -1);
  assert.ok(deadZone(0.5) > 0 && deadZone(0.5) < 0.5);
});
