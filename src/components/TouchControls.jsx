/** Pointer-captured pad supports touch and releases input on cancellation. */
export const TouchControls = ({ input }) => {
  const press = (event, x, y) => {
    event.currentTarget.setPointerCapture(event.pointerId);
    input.current.touch = { x, y };
  };
  const release = () => { input.current.touch = { x: 0, y: 0 }; };
  return <div className="touch-pad" aria-label="Commandes tactiles">
    {[[0, -1, '↑', 'Avancer'], [-1, 0, '←', 'Gauche'], [0, 1, '↓', 'Reculer'], [1, 0, '→', 'Droite']].map(([x, y, icon, label]) => <button key={label} aria-label={label} onPointerDown={e => press(e, x, y)} onPointerUp={release} onPointerCancel={release} onLostPointerCapture={release}>{icon}</button>)}
  </div>;
};
