import { useEffect, useRef } from "react";

/** Collect physical input without React updates in the animation loop. */
export const useInput = (onAction) => {
  const input = useRef({
    keys: new Set(),
    touch: { x: 0, y: 0 },
    orbit: 0,
    action: onAction,
  });
  input.current.action = onAction;
  useEffect(() => {
    const controls = new Set([
      "KeyW",
      "KeyA",
      "KeyS",
      "KeyD",
      "KeyZ",
      "KeyQ",
      "ArrowUp",
      "ArrowDown",
      "ArrowLeft",
      "ArrowRight",
      "Space",
      "ShiftLeft",
      "ShiftRight",
      "KeyE",
    ]);
    const down = (event) => {
      if (
        event.target.closest(
          'input, textarea, select, [contenteditable="true"], dialog',
        )
      )
        return;
      if (event.code === "Space" && event.target.closest("button, a")) return;
      if (controls.has(event.code)) event.preventDefault();
      input.current.keys.add(event.code);
      if (event.code === "KeyE" && !event.repeat) input.current.action();
    };
    const up = (event) => input.current.keys.delete(event.code);
    const clear = () => {
      input.current.keys.clear();
      input.current.touch = { x: 0, y: 0 };
    };
    window.addEventListener("keydown", down);
    window.addEventListener("keyup", up);
    window.addEventListener("blur", clear);
    document.addEventListener("visibilitychange", clear);
    return () => {
      window.removeEventListener("keydown", down);
      window.removeEventListener("keyup", up);
      window.removeEventListener("blur", clear);
      document.removeEventListener("visibilitychange", clear);
    };
  }, []);
  return input;
};
