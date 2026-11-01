export const JOINTS = ["LeftArm", "RightArm", "LeftLeg", "RightLeg", "Head"];
// Blender adds numeric suffixes; glTFLoader removes dots from node names.
export const jointName = (name) =>
  JOINTS.find((joint) => new RegExp(`^${joint}(?:[._]?\\d+)?$`).test(name));
