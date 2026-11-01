# Reference-led playable — 2026-11-01

This rebuild replaces the rejected first playable at `f9d17a3`. The user supplied three concept images and required a different stylized avatar, a completed/harmonized zeppelin and the full career rather than two grouped experiences. Visual acceptance remains with the user.

## Runtime

React 19 / R3F / Drei / Three / Vite, with exact versions in the lockfile. The scene loads nine Draco-compressed Blender dioramas, an original articulated traveller and an adapted passenger zeppelin. Decoder files are served locally. All physical scenery is actual 3D; the generated day/evening cloud imagery is only the distant background. Asset provenance and regeneration notes: [ASSETS.md](ASSETS.md).

`world.js` owns nine destinations, narrative content, boarding anchors and ship berths. `Journey.jsx` owns walking, takeoff, free/guided flight, assisted landing and the damped camera. Berths sit beside the pier; boarding tests use the pedestrian anchor. Keyboard, mouse orbit, touch and gamepad adapters are retained. Two ambient walkers share the new character geometry and can open the chapter journal.

`App.jsx` provides compact departure copy, nine-stop navigation, day/evening controls, help and reduced motion. `Journal.jsx` uses a native focus-trapped dialog. `scripts/build-carnet.mjs` builds the independent no-JS/no-WebGL text edition from the same nine chapter definitions, preventing another reduced-content fallback.

## Content

Caravan Atlas supplies: warehouse → masonry → agriculture → Club Med trapeze → ten years of circus → self-taught learning → O’Clock → development. Backroads is included as professional experience per the user; role and dates are not invented. Map placement is editorial, not a dated timeline. Animology is in conception; no unverified demonstrations or features are claimed.

## Validation and limits

Six tests cover all requested chapters and models, Draco exports, character joints, safe boarding points, island boundaries, main-building collision and analog drift. Production build passes. Browser QA checks the long guided route to the warehouse, keyboard movement and boarding distance, all nine journal entries, Escape/focus restoration, day/evening and desktop/mobile layouts. See `QUALITY_LOOP_REPORT.md` for visual corrections and evidence.

Walking collision is an island boundary plus a main-building exclusion, not a complete physics mesh for every prop. Body motion is procedural, not authored performance clips. Only two ambient people are interactive; no complex NPC dialogue, audio or CMS. Physical gamepad/mobile hardware and low-end GPU performance are not certified. All 11 GLBs total approximately 26 MB uncompressed HTTP payload; the visible loader reports asset progress.

The editable Blender scene is local under `artifacts/blender/`; source factory files are untouched. Source and runtime assets are tracked in the private GitHub repository, and publication uses the existing private Sites identity. GitHub-triggered deployment is not connected.
