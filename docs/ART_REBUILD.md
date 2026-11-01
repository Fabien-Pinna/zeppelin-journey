# Reference-led graphic rebuild

Authorized 2026-11-01 after explicit rejection of the `4f68a25` visuals. That Git revision and `artifacts/art-rebuild/baseline/walking.png` preserve the pre-rebuild result. The camera/navigation implementation remains the behavioral baseline.

## Reference contract

`2.png` supplies the floating-archipelago composition, pale eroded limestone cliffs, layered foliage and cream/teal/brass airship. `1.png` supplies sculpted architecture, individual stone and timber construction, populated workspaces and warm light. `3.png` supplies the curved conservatory and contrasting amber/blue-hour lighting. These are different perspective illustrations, not registered orthographic views: pixel silhouette IoU and exact object correspondence are inapplicable. Personal Vaucluse, Club Med and Bouglione facts supersede the illustrations' generic farm.

## Repair sequence and gates

1. Replace sphere-cluster foliage with branching canopies and shaped leaves; replace faceted boulder islands with stratified eroded cliff surfaces and hanging vegetation. Ground dressing must leave existing routes clear.
2. Replace uniform material color with exported base-color, normal and roughness maps. Wood grain, chalky stone, canvas, leather and aged brass must read separately at walking distance. No Blender-only procedural shader may be counted as runtime detail.
3. Rebuild the atelier as a curved glass conservatory and the tent as draped canvas; refine shared masonry, roof tiles and timber construction. Preserve semantic colliders, moving-part names and character grip positions.
4. Calibrate sunlight, sky fill, soft contact shadows and local amber practical lights in the actual browser. Do not use fog/bloom to conceal geometry errors.
5. Compare exported hero assets and actual playable day/evening scenes against all three references. Inspect all nine environments, walking/flight controls and animation bindings. Run the repository checks and publish only the validated result.

Existing reference-to-3d, material and look-calibration skills cover these failures; no generic skill modification is justified. Use isolated background Blender builds so the user's live source scene remains intact. Geometry is authored in Y-up coordinates and converted to Blender Z-up by `Batch.mesh`; exports return to Y-up. Changes to shared functions propagate to every chapter.

## Acceptance evidence

- The final twelve Draco/WebP GLBs contain 3,439,484 triangles before runtime instances and total 21,290,656 bytes (previous library approximately 27.8 MB). Per-asset counts are saved locally in `artifacts/art-rebuild/optimized/manifest.json`. No mesh simplification was used; small subpixel beads use fewer segments while large curved forms retain smooth geometry.
- `artifacts/art-rebuild/nine-chapters.png` compares all nine exported environments under the same review lighting. Separate `atelier-walking.png`, `traveller-overview.png`, `acrobat-overview.png` and `zeppelin-overview.png` inspect the detailed assets. The imported GLBs, rather than the authoring viewport, supply these renders.
- `browser-day.png` and `browser-night.png` in the same directory capture the actual Pages-base production build in Chrome: transparent conservatory, irregular paving, planted shoulders, readable traveller, timber pier, cream/brass airship and warm local lantern illumination. Walking and boarding controls remain available. Browser console has no JavaScript errors; an existing dependency warning about `THREE.Clock` remains.
- Corrected successive visible defects: directional texture striping, regular rim stones, uniform paving, oversized hair forelock, and double gamma conversion of exported base-color maps. `pre-color-fix/` preserves intermediate renders. `python scripts/check-art-textures.py` rejects the faulty export and passes all 23 checked decoded WebP palette values after correction (Pillow required).
- `npm test`: 28 passing tests, including all nine accessible guide routes, animation names, propeller/rig contracts, collisions, follow-camera behavior and ship occlusion. Asset checks now also require WebP plus exported color/normal/roughness maps for stone and wood. `PAGES_BASE_PATH=/zeppelin-journey/ npm run build`: passes.
- Remaining differences from the concept illustrations: scenery is still stylized, layouts and plant density favor playable space, and the illustrations' background cities, waterfalls and crowd density are not reproduced. The personal chapter facts supersede generic concept props. Physical mobile/gamepad and low-end GPU performance remain unmeasured; background-tab throttling is not a reliable performance benchmark. A technical validation is not the user's subjective visual acceptance.
