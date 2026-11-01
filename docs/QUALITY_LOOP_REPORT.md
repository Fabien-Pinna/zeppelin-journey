# Reference-led rebuild

The user rejected the design at `f9d17a3`. Preserve it in Git as failed visual evidence, not an accepted design baseline. References: `1.png`, `2.png`, `3.png`; prior runtime screenshots: `artifacts/first-playable*.png`.

Failure dimensions: silhouette/detail, material richness, environmental composition, and incomplete career coverage. The previous implementation mistook a navigation prototype for a sufficient response to a rich visual brief. It reduced the career to three destinations and had no Blender-authored environment.

Skill-gap decision: existing reference-to-3D, modeling, material, export and visual-validation workflows already address these failures. No shared skill patch is required. Correct the project, using the manifest gates and browser evidence before claiming completion.

The concepts are different perspective scenes, so exact multiview contour intersection and mask IoU would be misleading. Compare the actual composition, distinct silhouettes, material categories, foliage density, atmospheric depth and complete chapter inventory instead.

Implementation target: detailed Blender-authored reusable assets exported as GLB; frame-driven navigation retained where correct; complete career data; a rebuilt immersive UI with minimal scene obstruction. No concept illustration will be represented as a working 3D scene.

## Implemented second art pass

- Nine physical dioramas and nine independent narrative entries now cover the requested career. Shared content also generates the text-only edition.
- The supplied avatar is no longer rendered. A new original traveller has a teal jacket, rust scarf, backpack, boots, facial features and articulated procedural motion.
- The existing steampunk zeppelin was adapted, repaletted and completed with a glazed cabin, boarding steps and luggage. Warship features were removed. Source files are unchanged.
- Blender/material inspection caught a jagged envelope stripe, floating decorative ribs, repetitive grass textures and washed-out texture colors; these were corrected before final export. Rocks, planting, roof detailing and the overview camera were revised after browser comparison.
- Production browser QA verified port → warehouse takeoff/flight/landing, keyboard walking with the boarding action disabled away from the pier, all nine journal entries and Escape, day/evening, 1440×900 desktop and 390×844 responsive layouts. Browser console showed no runtime errors during these checks; a dependency Clock deprecation warning remains.
- Six tests and the production build pass. Physical gamepad/touch hardware and low-end device frame rates remain unverified. Exact concept-image fidelity and user visual acceptance are not claimed.

Editable local source: `artifacts/blender/zeppelin-journey-v2.blend`. Browser proof is stored under ignored `artifacts/v2-*.png`. See `ASSETS.md` for asset provenance and `implementation.md` for remaining system limits.

A post-publication check exposed a recoverable React `removeChild` error while the Drei HTML loading portal was being removed. The loader now lives in the ordinary DOM next to the canvas and remains visible until the scene has committed; the 3D Suspense boundary has no HTML portal fallback. This avoids competing portal cleanup during startup. The compact mobile overview was also reframed to keep the airship above the departure card.


## Living dioramas pass — 2026-11-01

User-authorized scope: life in all nine dioramas, chapter conversations, visible trapeze performer, more physical interaction, zoom, and placement cleanup.

Implemented: nine distinct animated activities, nine guides with three questions each, shared pause-aware simulation time, gravity-driven trapeze pendulum with rigid hand/bar coupling, a backpack-free artist costume, continuous parabolic juggling throws, animated glTF windmill/sheep/clock pivots, collider manifest exported with Blender models, substepped walking/sliding, jump/gravity, camera obstruction avoidance, wheel/buttons/keyboard/pinch zoom and touch jump.

Repairs: lamps moved away from Club Med loungers, the atelier display, O’Clock desks and Backroads van; atelier desks moved inside pavilion walls; bunting pole moved away from the farm fence; the ladder gained inclined supports and a platform; a central trapeze crossbeam and a larger independently anchored net were added. The mechanic was moved clear of the workbench. In-scene chapter labels now appear only in the overview so they do not cover performances. The dialogue was centred after mobile/desktop checks. A Blender suffix/Three.js sanitization mismatch in the second costume was found in browser QA, fixed and given a regression test.

Verification: 14 tests cover exported assets and joint binding, all nine docking/guide approaches, fast movement against thin poles, wall sliding, boundary limits, post/furniture clearances, worker paths, continuous/non-intersecting juggling trajectories, camera obstruction and pendulum frame independence. A five-minute pendulum run (maximum swing about 33.9 degrees; feet at least 2.60 m high over the 1.8 m net) checks hand contact, vertical clearance and the full body envelope above the net. Blender numeric inspection confirms that the bar grip lies inside each hand mesh. Browser checks cover actual trapeze poses, mobile dialogue, touch movement/jump, zoom, guide conversation and a guided tour of the other activities. Evidence lives in ignored `artifacts/life-*` screenshots and `artifacts/trapeze-grip-inspection.json`.

Limits: fixed props use simplified semantic boxes/cylinders, not exact triangle collision or pushable rigid bodies; tiny vegetation is non-solid. Dialogue is text. Physical multitouch and gamepad hardware, low-end GPUs and subjective visual perfection are not certified. User visual acceptance is not assumed.
