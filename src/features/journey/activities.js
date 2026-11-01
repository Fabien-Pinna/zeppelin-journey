export const activities = {
  atelier: {
    position: [2.5, 0.02, 2.2],
    rotation: Math.PI,
    pose: "create",
    color: "#b77f50",
  },
  warehouse: {
    position: [-0.6, 0.02, 4.8],
    rotation: Math.PI / 2,
    pose: "carry",
    color: "#be9b4b",
  },
  masonry: {
    position: [0.5, 0.02, 2],
    rotation: Math.PI,
    pose: "hammer",
    color: "#b48d68",
  },
  farm: {
    position: [-5.8, 0.02, 0.45],
    rotation: 0,
    pose: "garden",
    color: "#738b52",
  },
  circus: {
    position: [0, 0.02, -0.2],
    rotation: 0,
    pose: "juggle",
    color: "#aa5149",
  },
  backroads: {
    position: [-1, 0.02, 2],
    rotation: Math.PI,
    pose: "repair",
    color: "#7e934e",
  },
  learning: {
    position: [2, 0.02, 4.2],
    rotation: Math.PI,
    pose: "read",
    color: "#b28a59",
  },
  oclock: {
    position: [4.1, 0.02, -0.8],
    rotation: Math.PI,
    pose: "teach",
    color: "#789fa3",
  },
};

export const activityPosition = (id, time = 0) =>
  id === "warehouse"
    ? [-0.6 + Math.sin(time * 0.42) * 1.6, 0.02, 4.8]
    : activities[id]?.position;
