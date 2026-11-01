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
