import { assetUrl } from "../assetUrl.js";
import { useEffect, useRef } from "react";
import { exhibits, islands } from "../features/journey/world.js";

/** Native modal keeps focus inside the journal and restores it on close. */
export const Journal = ({ selection, onClose, onTravel }) => {
  const ref = useRef();
  useEffect(() => {
    if (selection && !ref.current.open) ref.current.showModal();
    else if (!selection && ref.current.open) ref.current.close();
  }, [selection]);
  const entries =
    selection === "all" ? islands : islands.filter((i) => i.id === selection);
  return (
    <dialog
      ref={ref}
      className="journal"
      onCancel={onClose}
      onClose={onClose}
      onClick={(e) => {
        if (e.target === ref.current) onClose();
      }}
    >
      <div className="journal-inner">
        <header className="flex items-center justify-between gap-4">
          <span className="eyebrow">Le carnet de Fabien</span>
          <button
            className="icon-button"
            onClick={onClose}
            aria-label="Fermer le carnet"
          >
            ×
          </button>
        </header>
        <h2>
          {selection === "all"
            ? "Chaque détour a son histoire."
            : exhibits[selection]?.title}
        </h2>
        <p className="journal-intro">
          Du geste au code, un voyage entre savoir-faire et curiosité.
        </p>
        {entries.map((island) => {
          const exhibit = exhibits[island.id];
          return (
            <article key={island.id}>
              <span className="eyebrow">{exhibit.label}</span>
              {selection === "all" && <h3>{exhibit.title}</h3>}
              {exhibit.paragraphs.map((p) => (
                <p key={p}>{p}</p>
              ))}
              <div className="tags">
                {exhibit.tags.map((tag) => (
                  <span key={tag}>{tag}</span>
                ))}
              </div>
              <div className="journal-foot">
                <small>{exhibit.note}</small>
                <button
                  className="text-button"
                  onClick={() => onTravel(island.id)}
                >
                  Visiter l’escale <span>↗</span>
                </button>
              </div>
            </article>
          );
        })}
        <a className="plain-link" href={assetUrl("projects.html")}>
          Ouvrir la version sans 3D ↗
        </a>
      </div>
    </dialog>
  );
};
