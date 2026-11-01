# First playable — 2026-11-01

## Direction

Floating islands + miniature theatre + a warm festival atmosphere. The initial scene prioritizes navigation and recognizable destinations. This is a playable foundation, not the final asset fidelity shown in the concept images.

Design tokens: ink `#263e42`, sky `#bdd4d2`, brass `#e8b45d`, teal `#478a89`, foliage `#7fa37a`, coral `#c76a64`. Outfit display type gives the interface a rounded travel-poster character; DM Sans handles controls and reading. The signature is the gold/teal zeppelin crossing a continuous 3D world. On desktop, the opening copy occupies the left side; on narrow screens, the copy sits over a bottom scrim. World-space labels open a readable journal.

## Systems and boundaries

- `src/App.jsx`: UI state, lazy scene boundary, journal, route selection, lighting and accessibility options.
- `src/features/journey/Journey.jsx`: mutable frame state for walking, takeoff, flight, landing and camera. UI telemetry is sampled, not written on every frame.
- `world.js`: island definitions, content, boarding anchors, collision constraints and input utilities.
- `useInput.js`: keyboard and touch state, focus/visibility cleanup. Gamepad polling lives in the frame loop.
- `Avatar.jsx`: cloned Ready Player Me skeleton, procedural arm and leg motion.
- `src/features/world`: original procedural scenery and airship. No Blender project or asset from Zeppelin Factory is claimed as integrated.
- `public/projects.html`: independent semantic portfolio, works with JavaScript and WebGL disabled.

Navigation states: overview → walking → takeoff → flying → landing → walking. Guided routes use the same takeoff and landing states. Free flight stays above the islands and inside the bounded world. Walking is constrained to an island and resolves the main building collision. Small props are decorative and do not yet have individual colliders.

## Content provenance

The Caravan Atlas specification provides the narrative chain: warehouse, masonry, agriculture, Club Med trapeze, ten years of circus, self-taught learning, O’Clock and development. Its WordPress dependency and old package versions are not inherited.

Backroads is a professional experience per the user's explicit correction. Exact title, dates and responsibilities are unknown; the interface does not invent them. Travel/cycling scenery is a visual interpretation.

Animology replaces Languology. The owning project overview describes an animal encyclopedia in conception, so the exhibit says “En conception” and does not present requested app features as working demos. No invented project URLs or contact details are used.

## Validation and limits

- Production build and focused navigation tests cover reachable docks, island boundaries, building exclusion and analog drift.
- Browser verification covers the avatar, guided transit, free takeoff/landing, journal, day/night and responsive layouts; see the project memory state for final observed results.
- A physical gamepad and phone still need device testing. No measured 60/30 fps claim is made.
- The 3D bundle is loaded separately from the UI. DPR is capped at 1.5; the avatar is about 1.1 MB. Scene scaling/instancing and finer GPU profiling remain work before extending the archipelago.
- Ambient animation currently includes propellers, gentle NPC movement and a trapeze. No audio, conversational NPCs, individual prop physics, production animation clips or CMS exists yet.
- The three island exhibits form the first pilot loop. Complete career dioramas, curated web/agent projects, richer interactions and final asset production remain subsequent milestones.

## Next work

1. Validate the movement feel with the user and tune the pilot island against the selected concepts.
2. Replace procedural avatar motion with suitable licensed clips; add terrain-aware locomotion.
3. Source the Backroads biography and select actual project demos.
4. Produce richer authored scenery, NPC interactions and the complete professional chapters.
5. Profile representative mobile hardware, instance repeated props and add quality presets.
6. Connect GitHub-triggered production publication once a durable deployment integration is available; the Sites source workflow currently performs explicit publication.
