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

## Aft flight, organic cast and personal places — 2026-11-01

The user again rejected low-poly simplification. The previous shipped assets remain in Git and the initial four detail targets were copied to `artifacts/detail-baseline/`. This pass replaces the primitive character anatomy with smooth custom profiles and curved forms, adds facial/clothing/hair detail, anatomical sheep and independent head/leg pivots, and two detailed independently rotating longitudinal propellers. Flight uses a damped aft chase camera across takeoff, cruise and landing; bounded manual orbit returns behind the ship after inactivity. Propellers spool/coast and share the paused simulation clock.

The first character render exposed broom-like hair and shoulder gaps; a second pass corrected the scalp/locks and sleeve joins. Wool normal mapping caused visible atlas facets and was removed in favor of shaped fleece/curls. A review-only quaternion/Euler mismatch produced a false grip failure; setting imported objects to Euler before posing resolved it. Both hands' exported skin bounds contain the grip height 2.33. Three propeller angle renders and their contact sheet show stable silhouettes, with no automated flicker warning; actual browser flight frames also show blade motion. Close-ups of the new circus animals led to removing a patchy elephant skin map and replacing the lion's sparse mane with layered curved locks, eyes/lids and an untextured muzzle material. Before-images are preserved.

New user facts replace generic scenery: three Vaucluse crops and pale Ventoux ridge; Gregolimano/Beldi shoreline, sailing/waterskiing/pool/open-air theatre and the documented three-gantry flying rig; Bouglione touring tent, Paris venue vignette, caravans, announcement truck, rigging stock/control desk, performers and animals. Narratives explicitly distinguish Fabien's backstage jobs from the artists. All nine island outlines differ. Browser inspection led to moving the lion away from the parked ship's occlusion and replacing an overly craggy mountain blockout with a broad limestone ridge. Exported overview inspection also caught a side guy crossing the pier and a pine in the pool: the rig/shore were moved left, pine trunks moved clear, and placement regressions now cover trees, parasols, signs, pools, stage and seats. Freestanding signs gained supports.

Twenty tests pass, including aft camera at every heading/orbit limit, propeller start/pause/stop, exported articulated parts, all nine shaped boundaries, shoreline/pool exclusion, rig dimensions, guide/worker/extra cast clearances and the existing navigation checks. The updated five-minute flying-trapeze run keeps feet above the 2.032 m net by at least 0.18 m and within its longitudinal envelope. Production build passes. Browser evidence: `artifacts/detail-review/flight-live-*.png`, `farm-live.png`, `circus-live.png` and final published screenshots.

Remaining limits: stylized real-time geometry is richer but does not reproduce the concept images' painterly density or certify photorealism. The circus facade and two-resort island are evocations. Fixed props still use semantic collision shapes; thin rigging, foliage and miniature sea craft are decorative. Animal motion is idle/grazing/trunk movement, not a full locomotion rig; trapeze artists swing without a release/catch stunt. Low-end hardware and physical controllers remain unmeasured. User acceptance is not presumed.

## Walking camera elevation — 2026-11-01

Added at the user's explicit request after the personal-landscapes release: vertical mouse/touch drag and right-stick Y adjust camera elevation while walking. Pitch is bounded above the ground and below the vertical pole; distance is conserved, with the existing zoom and obstacle avoidance retained. The recenter control restores the former 14 m horizontal / 6.7 m vertical offset from the look target. 21 tests and the build pass. Browser inspection verifies high/low views and reset; evidence is under `artifacts/detail-review/camera-walk-*.png`. Physical gamepad hardware remains unverified.
