import { useEffect, useRef } from "react";
import { clampZoom } from "./physics.js";
import { DEFAULT_WALK_PITCH } from './camera.js';

/** Collect physical input without React updates in the animation loop. */
export const useInput = (onAction, onTalk) => {
  const input = useRef({
    keys: new Set(),
    touch: { x: 0, y: 0 },
    orbit: 0,
    lookVersion: 0,
    recenterVersion: 0,
    pitch: DEFAULT_WALK_PITCH,
    zoom: 1,
    jump: false,
    action: onAction,
    talk: onTalk,
  });
  input.current.action = onAction;
  input.current.talk = onTalk;
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
      "KeyF",
      "Equal",
      "Minus",
      "NumpadAdd",
      "NumpadSubtract",
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
      if (event.code === "KeyF" && !event.repeat) input.current.talk?.();
      if (["Equal", "NumpadAdd"].includes(event.code))
        input.current.zoom = clampZoom(input.current.zoom / 1.12);
      if (["Minus", "NumpadSubtract"].includes(event.code))
        input.current.zoom = clampZoom(input.current.zoom * 1.12);
    };
    const up = (event) => input.current.keys.delete(event.code);
    const clear = () => {
      input.current.keys.clear();
      input.current.touch = { x: 0, y: 0 };
      input.current.jump = false;
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
