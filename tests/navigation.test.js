import test from "node:test";
import assert from "node:assert/strict";
import {
  islands,
  dockPosition,
  nearestIsland,
  deadZone,
} from "../src/features/journey/world.js";
import {
  moveWalker,
  obstaclesFor,
  penetration,
  GUIDE_POSITION,
  createPendulum,
  stepPendulum,
  trapezePoint,
  TRAPEZE,
  clampZoom,
} from "../src/features/journey/physics.js";
import { conversations } from "../src/features/journey/conversations.js";

test("every harbour is clear and selected by assisted docking", () => {
  for (const island of islands) {
    const [x, , z] = dockPosition(island);
    assert.deepEqual(moveWalker(x, z, 0, 0, island, 0.2), [x, z]);
    assert.equal(nearestIsland(x, z).island.id, island.id);
  }
});
test("large motion cannot tunnel through a thin pole or leave an island", () => {
  const island = islands[0];
  const [x] = moveWalker(-8, -1, 3, 0, island);
  assert.ok(x <= -7.42 + 0.001, "lantern must stop the walker");
  for (const island of islands)
    for (let a = 0; a < Math.PI * 2; a += 0.3) {
      const [x, z] = moveWalker(
        ...[island.position[0] + 6, island.position[2] + 8],
        Math.cos(a) * 35,
        Math.sin(a) * 35,
        island,
      );
      assert.ok(
        Math.hypot(x - island.position[0], z - island.position[2]) <=
          island.radius - 0.89,
      );
    }
});
test("a diagonal approach slides along a building without entering it", () => {
  const island = islands.find((i) => i.id === "warehouse");
  const [x, z] = moveWalker(
    island.position[0] - 2,
    island.position[2] - 1,
    2,
    -3,
    island,
  );
  assert.ok(z >= island.position[2] - 1.68 - 0.001);
  assert.ok(x > island.position[0] - 1.5);
});
test("each guide can be approached from the arrival pier", () => {
  for (const island of islands) {
    let x = island.position[0] + 6,
      z = island.position[2] + 8;
    const tx = island.position[0] + GUIDE_POSITION[0],
      tz = island.position[2] + GUIDE_POSITION[2];
    for (let i = 0; i < 180; i++)
      [x, z] = moveWalker(x, z, (tx - x) * 0.03, (tz - z) * 0.03, island, 0.2);
    assert.ok(Math.hypot(x - tx, z - tz) < 2, island.id);
  }
});
test("posts no longer intersect chairs, desks or the van", () => {
  for (const island of islands) {
    const obstacles = obstaclesFor(island.id);
    for (const post of obstacles.filter((o) =>
      ["lantern", "bunting-post"].includes(o.name),
    )) {
      for (const prop of obstacles.filter((o) =>
        ["desk", "chair", "lounge-chair", "van", "display"].includes(o.name),
      )) {
        assert.equal(
          penetration(
            post.position[0],
            post.position[2],
            prop,
            post.size[0] / 2,
          ),
          null,
          `${island.id}: ${post.name} / ${prop.name}`,
        );
      }
    }
  }
});
test("pendulum retains grip and clears the net throughout a five-minute run", () => {
  const p = createPendulum();
  let minY = Infinity,
    maxAngle = 0;
  for (let frame = 0; frame < 60 * 300; frame++) {
    const a = stepPendulum(p, 1 / 60);
    maxAngle = Math.max(maxAngle, Math.abs(a));
    const bar = trapezePoint(a, [0.36, -TRAPEZE.length, 0]);
    const hand = trapezePoint(a, [
      0.4 * 0.9,
      -TRAPEZE.length - 2.33 * 0.9 + (1.64 + 0.69) * 0.9,
      0.02 * 0.9 - 0.02 * 0.9,
    ]);
    assert.ok(Math.hypot(...bar.map((n, i) => n - hand[i])) < 0.00001);
    const foot = trapezePoint(a, [0, -TRAPEZE.length - 2.33 * 0.9, 0.018]);
    minY = Math.min(minY, foot[1]);
    assert.ok(
      Math.abs(foot[2] + 2.5) + 0.35 < 3.1,
      "full body stays over the safety net",
    );
  }
  assert.ok(minY > 2.5, `feet ${minY}, net 1.8`);
  assert.ok(maxAngle > 0.5 && maxAngle < 1.1, `stable amplitude ${maxAngle}`);
});
test("pendulum timing agrees at 30 and 120 FPS", () => {
  const a = createPendulum(),
    b = createPendulum();
  for (let i = 0; i < 300; i++) stepPendulum(a, 1 / 30);
  for (let i = 0; i < 1200; i++) stepPendulum(b, 1 / 120);
  assert.ok(Math.abs(a.angle - b.angle) < 0.00001);
});
test("all nine guides have distinct complete conversations; zoom is bounded", () => {
  for (const i of islands) {
    assert.ok(conversations[i.id].greeting.length > 50);
    assert.equal(conversations[i.id].topics.length, 3);
    assert.equal(new Set(conversations[i.id].topics.map(([q]) => q)).size, 3);
  }
  assert.equal(clampZoom(0.1), 0.55);
  assert.equal(clampZoom(10), 1.8);
  assert.equal(deadZone(0.1), 0);
  assert.equal(deadZone(1), 1);
});

test("workers and guides remain clear of fixed props throughout their loops", () => {
  for (const island of islands)
    for (let time = 0; time < 45; time += 0.4) {
      const objects = obstaclesFor(island.id, time);
      for (const actor of objects.filter((o) =>
        ["worker", "guide"].includes(o.name),
      )) {
        for (const obstacle of objects.filter(
          (o) => !["worker", "guide", "sheep-a", "sheep-b"].includes(o.name),
        )) {
          assert.equal(
            penetration(actor.position[0], actor.position[2], obstacle, 0.3),
            null,
            `${island.id}: ${actor.name} / ${obstacle.name}`,
          );
        }
      }
    }
});
test("camera stops before an intervening wall", async () => {
  const { cameraFraction } = await import("../src/features/journey/physics.js");
  const island = islands.find((i) => i.id === "warehouse"),
    [x, y, z] = island.position;
  const fraction = cameraFraction(
    [x - 2, y + 1.3, z],
    [x - 2, y + 2, z - 8],
    island,
  );
  assert.ok(fraction > 0.1 && fraction < 0.3);
  assert.equal(
    cameraFraction([x, y + 2, z + 6], [x, y + 8, z + 20], island),
    1,
  );
});

test('juggling throws stay continuous and the three balls do not intersect', async () => {
  const { jugglingBall } = await import('../src/features/journey/physics.js');
  for (let time=0;time<12;time+=.01) {
    const balls=[0,1,2].map(i=>jugglingBall(time,i));
    for (let i=0;i<3;i++) {
      const next=jugglingBall(time+.00001,i);
      assert.ok(Math.hypot(...balls[i].map((n,k)=>n-next[k]))<.001);
      for(let j=i+1;j<3;j++) assert.ok(Math.hypot(...balls[i].map((n,k)=>n-balls[j][k]))>.21);
    }
  }
});
