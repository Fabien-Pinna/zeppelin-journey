import {
  lazy,
  Suspense,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";
import { ErrorBoundary } from "react-error-boundary";
import { Journal } from "./components/Journal.jsx";
import { TouchControls } from "./components/TouchControls.jsx";
import { useInput } from "./features/journey/useInput.js";
import { islands } from "./features/journey/world.js";

const World = lazy(async () => ({
  default: (await import("./features/world/World.jsx")).World,
}));

/** Portfolio shell, accessible navigation and journey state transitions. */
export const App = () => {
  const [mode, setMode] = useState("overview");
  const [islandId, setIslandId] = useState("atelier");
  const [destination, setDestination] = useState(null);
  const [journal, setJournal] = useState(null);
  const [mapOpen, setMapOpen] = useState(false);
  const [night, setNight] = useState(false);
  const [reduced, setReduced] = useState(
    () => window.matchMedia("(prefers-reduced-motion: reduce)").matches,
  );
  const [help, setHelp] = useState(false);
  const [status, setStatus] = useState({
    x: 6,
    z: 5,
    altitude: 1,
    near: "atelier",
    canBoard: true,
    canLand: true,
    gamepad: false,
  });
  const [sceneError, setSceneError] = useState(false);
  const actionRef = useRef(null),
    drag = useRef(null);
  const input = useInput(() => actionRef.current?.());
  const current = islands.find((i) => i.id === islandId);
  const intro = mode === "overview";
  const busy = mode === "takeoff" || mode === "landing" || Boolean(destination);
  const closeJournal = useCallback(() => setJournal(null), []);
  useEffect(() => {
    const change = () =>
      setReduced(window.matchMedia("(prefers-reduced-motion: reduce)").matches);
    const query = window.matchMedia("(prefers-reduced-motion: reduce)");
    query.addEventListener("change", change);
    const error = (event) => {
      if (String(event.message).match(/WebGL|GLTF|fetch.*model/i))
        setSceneError(true);
    };
    window.addEventListener("error", error);
    return () => {
      query.removeEventListener("change", change);
      window.removeEventListener("error", error);
    };
  }, []);
  const travel = (id) => {
    if (busy) return;
    setJournal(null);
    setMapOpen(false);
    if (id === islandId && (mode === "walking" || intro)) {
      setMode("walking");
      return;
    }
    setDestination(id);
    if (mode === "walking" || intro) setMode("takeoff");
  };
  const pointerDown = (event) => {
    if (intro || event.target.closest("button")) return;
    drag.current = event.clientX;
    event.currentTarget.setPointerCapture(event.pointerId);
  };
  const pointerMove = (event) => {
    if (drag.current === null) return;
    input.current.orbit -= (event.clientX - drag.current) * 0.006;
    drag.current = event.clientX;
  };
  return (
    <main
      className={`app ${intro ? "is-intro" : "is-playing"} ${night ? "is-night" : ""}`}
    >
      <a href="/projects.html" className="skip-link">
        Passer à la version sans 3D
      </a>
      <div
        className="scene"
        aria-label="Archipel flottant interactif"
        onPointerDown={pointerDown}
        onPointerMove={pointerMove}
        onPointerUp={() => {
          drag.current = null;
        }}
        onPointerCancel={() => {
          drag.current = null;
        }}
      >
        <ErrorBoundary
          fallback={
            <div className="canvas-fallback">
              La 3D n’a pas pu démarrer.{" "}
              <a href="/projects.html">Lire le carnet de voyage ↗</a>
            </div>
          }
        >
          {!sceneError ? (
            <Suspense
              fallback={
                <div className="loading">
                  <span className="loading-orbit">✦</span>Préparation de votre
                  voyage…
                </div>
              }
            >
              <World
                mode={mode}
                setMode={setMode}
                islandId={islandId}
                setIslandId={setIslandId}
                destination={destination}
                setDestination={setDestination}
                input={input}
                actionRef={actionRef}
                telemetry={setStatus}
                night={night}
                reduced={reduced}
                paused={Boolean(journal || help || mapOpen)}
                onExhibit={setJournal}
              />
            </Suspense>
          ) : (
            <div className="canvas-fallback">
              La 3D n’a pas pu démarrer.{" "}
              <a href="/projects.html">Lire le carnet de voyage ↗</a>
            </div>
          )}
        </ErrorBoundary>
      </div>
      <div className="vignette" />
      <header className="topbar">
        <a href="/" className="brand" aria-label="Zeppelin Journey, accueil">
          <span className="brand-mark">✣</span>
          <span>
            ZEPPELIN<span className="brand-sub">JOURNEY</span>
          </span>
        </a>
        <nav
          className="flex items-center gap-2"
          aria-label="Navigation principale"
        >
          <button
            className={`nav-button ${mapOpen ? "active" : ""}`}
            aria-expanded={mapOpen}
            onClick={() => {
              setMapOpen(!mapOpen);
              setHelp(false);
            }}
          >
            Les escales <span>↗</span>
          </button>
          <button
            className="nav-button journal-button"
            onClick={() => setJournal("all")}
          >
            Le carnet <span>↗</span>
          </button>
          <span className="nav-divider" />
          <button
            className="icon-button"
            onClick={() => setNight(!night)}
            aria-label={night ? "Passer au jour" : "Passer à la nuit"}
            title={night ? "Ambiance de jour" : "Ambiance de nuit"}
          >
            {night ? "☾" : "☀"}
          </button>
        </nav>
      </header>
      {intro && (
        <section className="intro-copy">
          <div className="eyebrow intro-eyebrow">
            <span /> Le portfolio de Fabien
          </div>
          <h1>
            D’un univers <em>à l’autre.</em>
          </h1>
          <p>Neuf escales, des métiers de terrain aux lignes de code.</p>
          <div className="intro-actions">
            <button
              className="primary-button start-button"
              onClick={() => setMode("walking")}
            >
              Commencer le voyage <span>↗</span>
            </button>
            <button className="quiet-button" onClick={() => setJournal("all")}>
              Lire le carnet <span>→</span>
            </button>
          </div>
        </section>
      )}
      {mapOpen && (
        <section className="route-panel" aria-label="Choisir une escale">
          <div className="flex items-center justify-between">
            <span className="eyebrow">Votre archipel</span>
            <button
              className="icon-button"
              onClick={() => setMapOpen(false)}
              aria-label="Fermer les escales"
            >
              ×
            </button>
          </div>
          <h2>Où vous mène la curiosité ?</h2>
          <p className="route-intro">9 îles · Autant de chapitres à explorer</p>
          {islands.map((i) => (
            <button
              key={i.id}
              className="route-stop"
              disabled={busy}
              onClick={() => travel(i.id)}
            >
              <span className="stop-dot" style={{ background: i.color }}>
                {i.number}
              </span>
              <span>
                <b>{i.short}</b>
                <small>{i.chapter}</small>
              </span>
              <span>{i.id === islandId ? "●" : "↗"}</span>
            </button>
          ))}
          <p className="panel-note">
            Choisissez une île pour une traversée guidée.
          </p>
        </section>
      )}
      {!intro && (
        <>
          <section className="location-card">
            <span className="eyebrow">
              {mode === "walking" ? "Vous explorez" : "À bord du zeppelin"}
            </span>
            <h2>
              {mode === "walking"
                ? current.name
                : destination
                  ? `Cap sur ${islands.find((i) => i.id === destination)?.short}`
                  : "Entre ciel et possibles"}
            </h2>
            <span className="location-detail">
              <i />
              {mode === "walking"
                ? current.chapter
                : `${status.altitude} m · ${mode === "takeoff" ? "Décollage" : mode === "landing" ? "Atterrissage" : destination ? "Traversée guidée" : "Vol libre"}`}
            </span>
          </section>
          <div className="action-dock" aria-live="polite">
            {mode === "walking" ? (
              <>
                <button
                  className="primary-button"
                  disabled={!status.canBoard}
                  onClick={() => actionRef.current?.()}
                >
                  <kbd>E</kbd>{" "}
                  {status.canBoard ? "Embarquer" : "Rejoignez le ponton"}{" "}
                  <span>↑</span>
                </button>
                <button
                  className="secondary-button"
                  onClick={() => setJournal(islandId)}
                >
                  Découvrir l’escale ↗
                </button>
              </>
            ) : busy ? (
              <div className="travel-status">
                <span className="status-pulse" />
                {mode === "takeoff"
                  ? "On prend de la hauteur…"
                  : mode === "landing"
                    ? "Bienvenue à l’escale…"
                    : "Laissez-vous porter…"}
              </div>
            ) : (
              <>
                <button
                  className="primary-button"
                  disabled={!status.canLand}
                  onClick={() => actionRef.current?.()}
                >
                  <kbd>E</kbd>{" "}
                  {status.canLand ? "Atterrir" : "Approchez d’une île"}{" "}
                  <span>↓</span>
                </button>
                <button
                  className="secondary-button"
                  onClick={() => setMapOpen(true)}
                >
                  Choisir un cap ↗
                </button>
              </>
            )}
          </div>
          {!busy && <TouchControls input={input} />}
        </>
      )}
      <footer className="bottom-bar">
        <span className="edition">
          <i /> Fabien Pinna <span className="edition-separator">/</span> 9
          escales · Un parcours
        </span>
        <div className="footer-controls">
          <button
            className="quiet-button"
            onClick={() => setReduced(!reduced)}
            aria-pressed={reduced}
          >
            {reduced ? "◉" : "○"} Mouvements réduits
          </button>
          <button
            className="help-button"
            aria-label="Afficher les commandes"
            aria-expanded={help}
            onClick={() => {
              setHelp(!help);
              setMapOpen(false);
            }}
          >
            ?
          </button>
        </div>
      </footer>
      {help && (
        <section className="help-panel">
          <div className="flex items-center justify-between">
            <h2>Les commandes</h2>
            <button
              className="icon-button"
              onClick={() => setHelp(false)}
              aria-label="Fermer les commandes"
            >
              ×
            </button>
          </div>
          <dl>
            <dt>ZQSD / WASD / flèches</dt>
            <dd>Marcher · piloter</dd>
            <dt>Glisser la souris</dt>
            <dd>Regarder autour de soi</dd>
            <dt>E</dt>
            <dd>Embarquer · atterrir</dd>
            <dt>Espace / Maj en vol</dt>
            <dd>Monter · descendre</dd>
            <dt>Maj à pied</dt>
            <dd>Courir</dd>
            <dt>Manette</dt>
            <dd>
              Stick gauche : déplacement · droit : caméra · A : action ·
              gâchettes : altitude
            </dd>
          </dl>
          <p>
            {status.gamepad
              ? "Manette connectée"
              : "Sur mobile, utilisez les flèches à l’écran ou choisissez une traversée guidée."}
          </p>
          <a href="/projects.html">Lire le carnet sans 3D ↗</a>
        </section>
      )}
      <Journal selection={journal} onClose={closeJournal} onTravel={travel} />
    </main>
  );
};

