# Zeppelin Journey

A playable React Three Fiber portfolio: walk through a floating archipelago, board a zeppelin and travel between nine professional and creative chapters.

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
- Drag the scene: rotate the camera. Wheel, +/− buttons or pinch: zoom; centre button resets the view.
- F near the guide, or click their speech bubble: ask three chapter-specific questions.
- E: board near the dock, or land near an island.
- Space / Shift: ascend / descend in flight. Space: jump on foot; Shift: run.
- Standard gamepad: left stick movement, right stick camera, A action, triggers altitude.
- Touch: directional pad, action buttons and guided routes through the island menu.

The journal, conversations and navigation overlays pause movement and ambient activity. The reduced-motion option stops ambient animation and camera smoothing; a completely static reading experience is available through the no-3D version.

## Living archipelago

Nine detailed Blender dioramas cover development, warehouse work, masonry, agriculture, Club Med trapeze, ten years of circus, Backroads, self-taught learning and O’Clock. Every island has an animated worker or artist and an approachable guide. The physical pendulum carries the trapeze artist; other scenes include juggling, grazing sheep, a windmill, tool work, reading and teaching.

Walking uses a collider manifest exported from the same Blender geometry: walls, furniture, posts, crates and other solid props. Substepped movement slides along obstacles, with gravity, jumping and an island boundary. This is lightweight kinematic physics, not a rigid-body destruction simulation.

See [implementation notes](docs/implementation.md) for boundaries, content provenance and remaining work. The GitHub repository is public. The separate private Sites publication uses `.openai/hosting.json` and the Sites source workflow; GitHub pushes update GitHub Pages, not the Sites host.


## GitHub Pages

The public website is [Zeppelin Journey](https://fabien-pinna.github.io/zeppelin-journey/), from [Fabien-Pinna/zeppelin-journey](https://github.com/Fabien-Pinna/zeppelin-journey). `.github/workflows/pages.yml` runs the tests, builds the static site and publishes `dist` on pushes to `main` or a manual workflow dispatch. Pages uses GitHub Actions as its source.

`PAGES_BASE_PATH=/zeppelin-journey/` selects the Pages project subdirectory. Without that environment variable, builds keep the root path used by the existing Sites host. Public assets, Draco decoder and navigation use Vite's deployment base; the standalone journal links back relatively. No deployment token secret is required by the Pages workflow.
