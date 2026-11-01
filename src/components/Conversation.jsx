import { useEffect, useRef, useState } from "react";
import { conversations } from "../features/journey/conversations.js";
import { islands } from "../features/journey/world.js";

export function Conversation({ selection, onClose, onJournal }) {
  const dialog = useRef();
  const [topic, setTopic] = useState(null);
  const [visited, setVisited] = useState([]);
  const story = conversations[selection];
  const island = islands.find((i) => i.id === selection);
  useEffect(() => {
    setTopic(null);
    setVisited([]);
    if (selection && !dialog.current.open) dialog.current.showModal();
    else if (!selection && dialog.current.open) dialog.current.close();
  }, [selection]);
  return (
    <dialog
      ref={dialog}
      className="conversation"
      aria-labelledby="conversation-name"
      onCancel={onClose}
      onClose={onClose}
    >
      {story && (
        <div className="conversation-inner">
          <header>
            <span className="eyebrow">
              {story.role} · {island.number} / 09
            </span>
            <button
              className="icon-button"
              onClick={onClose}
              aria-label="Terminer la conversation"
            >
              ×
            </button>
          </header>
          <div className="speaker">
            <span className="speaker-icon" style={{ background: island.color }}>
              {island.icon}
            </span>
            <div>
              <small>Une voix de l’escale</small>
              <h2 id="conversation-name">{story.name}</h2>
            </div>
          </div>
          {topic !== null && (
            <p className="your-question">Vous · {story.topics[topic][0]}</p>
          )}
          <p className="spoken-text" aria-live="polite">
            {topic === null ? story.greeting : story.topics[topic][1]}
          </p>
          <div className="conversation-choices" aria-label="Vos questions">
            {story.topics.map(([question], index) => (
              <button
                key={question}
                aria-pressed={topic === index}
                onClick={() => {
                  setTopic(index);
                  setVisited((v) => [...new Set([...v, index])]);
                }}
              >
                <span>{question}</span>
                <span aria-hidden="true">
                  {visited.includes(index) ? "✓" : "↗"}
                </span>
              </button>
            ))}
          </div>
          <footer>
            <button
              className="text-button"
              onClick={() => onJournal(selection)}
            >
              Ouvrir le carnet ↗
            </button>
            <button className="primary-button" onClick={onClose}>
              À bientôt <span>→</span>
            </button>
          </footer>
        </div>
      )}
    </dialog>
  );
}
