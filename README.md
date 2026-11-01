# Zeppelin Journey

A playable React Three Fiber portfolio: walk through a floating archipelago, board a zeppelin and travel between three narrative stops.

## Run

Requires Node.js 22.12+ (developed on Node 24) and npm.

```sh
npm ci
npm run dev
npm test
npm run build
```

No environment variables or API keys are required. `npm run preview` serves the production build. `/projects.html` is the standalone no-JavaScript portfolio.

## Controls

- WASD, ZQSD or arrows: move; in flight, left/right steer and up/down propel.
- Drag the scene: rotate the camera.
- E: board near the dock, or land near an island.
- Space / Shift: ascend / descend in flight. Shift: run on foot.
- Standard gamepad: left stick movement, right stick camera, A action, triggers altitude.
- Touch: directional pad, action buttons and guided routes through the island menu.

The journal pauses movement. The reduced-motion option stops ambient animation and camera smoothing; a completely static reading experience is available through the no-3D version.

## First playable scope

Three islands: the port/workshop, Backroads and the theatre. Each has a dock, an exhibit and a guided flight destination. The supplied Ready Player Me avatar uses procedural rig animation; the source contains no animation clips. Scenery and the zeppelin are original procedural meshes, intended as the first navigable art pass.

See [implementation notes](docs/implementation.md) for boundaries, content provenance and remaining work. The GitHub repository is private. Sites publication uses `.openai/hosting.json` and the Sites source workflow; GitHub pushes alone do not currently publish the Site.
