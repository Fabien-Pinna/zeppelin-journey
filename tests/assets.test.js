import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import {
  islands,
  exhibits,
  berthPosition,
  dockPosition,
} from "../src/features/journey/world.js";

test("every requested career chapter has a distinct model and narrative", () => {
  assert.deepEqual(
    new Set(islands.map((i) => i.id)),
    new Set([
      "atelier",
      "warehouse",
      "masonry",
      "farm",
      "clubmed",
      "circus",
      "backroads",
      "learning",
      "oclock",
    ]),
  );
  const textEdition = readFileSync(
    new URL("../public/projects.html", import.meta.url),
    "utf8",
  );
  for (const island of islands) {
    assert.ok(exhibits[island.id].paragraphs.length >= 2);
    assert.ok(textEdition.includes(`id="${island.id}"`));
    const bytes = readFileSync(
      new URL(`../public/models/world-v2/${island.id}.glb`, import.meta.url),
    );
    assert.equal(bytes.toString("utf8", 0, 4), "glTF");
    const gltf = JSON.parse(
      bytes.toString("utf8", 20, 20 + bytes.readUInt32LE(12)),
    );
    assert.ok(gltf.extensionsRequired.includes("KHR_draco_mesh_compression"));
    assert.ok(gltf.meshes.length > 10);
    assert.ok(
      !gltf.nodes.some((n) => n.name === "Cube"),
      "default Blender scene must not leak into exports",
    );
    assert.ok(
      Math.hypot(
        berthPosition(island)[0] - dockPosition(island)[0],
        berthPosition(island)[2] - dockPosition(island)[2],
      ) > 5,
      "ship is parked beside the boarding point",
    );
  }
});

test("the new traveller includes the articulated limbs used by the runtime", () => {
  const bytes = readFileSync(
    new URL("../public/models/world-v2/traveller.glb", import.meta.url),
  );
  const gltf = JSON.parse(
    bytes.toString("utf8", 20, 20 + bytes.readUInt32LE(12)),
  );
  const names = new Set(gltf.nodes.map((n) => n.name));
  for (const name of [
    "Traveller",
    "Head",
    "LeftArm",
    "RightArm",
    "LeftLeg",
    "RightLeg",
  ])
    assert.ok(names.has(name), name);
});
