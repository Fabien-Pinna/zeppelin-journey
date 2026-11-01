/** Physical chapters and narrative share one source, including the text edition. */
export const islands = [
  [
    "atelier",
    "Création numérique",
    "Le port des possibles",
    "Développement & projets",
    [0, 0, 0],
    "#8eae9f",
    "✦",
  ],
  [
    "warehouse",
    "L’entrepôt",
    "Les premiers mouvements",
    "Expérience en entrepôt",
    [-65, 5, -77],
    "#c5a37a",
    "▤",
  ],
  [
    "masonry",
    "La maçonnerie",
    "Pierre après pierre",
    "Métier manuel",
    [-33, 8, -53],
    "#d2b79a",
    "⌑",
  ],
  [
    "farm",
    "L’agriculture",
    "Au rythme du vivant",
    "Travail agricole",
    [2, 7, -42],
    "#9eae6d",
    "❧",
  ],
  [
    "clubmed",
    "Le trapèze",
    "Le premier envol",
    "Trapèze · Club Med",
    [33, 4, -23],
    "#86babc",
    "⌁",
  ],
  [
    "circus",
    "Les années cirque",
    "Dix ans dans les airs",
    "Arts du cirque · 10 années",
    [-32, 3, -16],
    "#d78f79",
    "◒",
  ],
  [
    "backroads",
    "Backroads",
    "L’appel du voyage",
    "Expérience professionnelle",
    [-66, 8, -37],
    "#a9b985",
    "↗",
  ],
  [
    "learning",
    "L’autodidacte",
    "Apprendre, encore",
    "Apprentissage personnel",
    [-4, 12, -82],
    "#c7ae79",
    "✎",
  ],
  [
    "oclock",
    "O’Clock",
    "Un nouveau langage",
    "Formation au développement",
    [31, 10, -66],
    "#83aaa7",
    "◷",
  ],
].map(([id, short, name, chapter, position, color, icon], index) => ({
  id,
  short,
  name,
  chapter,
  position,
  color,
  icon,
  radius: 13,
  number: String(index + 1).padStart(2, "0"),
}));
const stories = {
  atelier: [
    "Le développement web ouvre un nouveau terrain de création après les métiers manuels, l’agriculture et les arts du cirque.",
    "Animology est un projet d’encyclopédie animale pour les enfants, imaginé pour une tablette Android. Dinosaures, fiches et exploration visuelle font partie de sa conception.",
  ],
  warehouse: [
    "Le parcours commence aussi dans les entrepôts. Cette expérience professionnelle a sa propre place dans l’archipel.",
    "Palettes, caisses et petit chariot composent cette escale consacrée au travail de terrain.",
  ],
  masonry: [
    "Avant les lignes de code, il y a eu la maçonnerie : un autre rapport à la construction, aux matériaux et au travail manuel.",
    "Une arche en cours d’assemblage et un atelier de pierre donnent forme à ce chapitre du parcours.",
  ],
  farm: [
    "Le travail agricole fait également partie du parcours. Une expérience à retrouver dans cette île de cultures, de végétation et de chemins de terre.",
    "La ferme et son moulin sont une évocation visuelle de ce chapitre.",
  ],
  clubmed: [
    "Le trapèze au Club Med marque une étape du parcours dans les airs.",
    "Cette escale s’organise autour d’un portique de trapèze et de son filet. Elle précède le long chapitre consacré au cirque.",
  ],
  circus: [
    "Dix années de cirque : un chapitre à part entière, après le trapèze au Club Med.",
    "Un chapiteau ouvert, une piste et des gradins forment le cœur de cette île dédiée aux arts du cirque.",
  ],
  backroads: [
    "Backroads fait partie de mon parcours professionnel et possède désormais son escale dédiée.",
    "Les vélos, le véhicule et la maison d’étape évoquent l’univers du voyage. La place de cette île sur la carte ne fixe pas de chronologie.",
  ],
  learning: [
    "L’apprentissage en autodidacte ouvre la voie à la création numérique.",
    "Livres, carnet et ordinateur se retrouvent dans un petit atelier : une escale pour cette phase d’exploration et d’apprentissage personnel.",
  ],
  oclock: [
    "La formation O’Clock prolonge l’apprentissage personnel et constitue une étape du parcours vers le développement.",
    "Une école, son horloge et un atelier collectif matérialisent ce chapitre, avant de retrouver les projets au port des possibles.",
  ],
};
export const exhibits = Object.fromEntries(
  islands.map((i) => [
    i.id,
    {
      title: i.name,
      label: i.chapter,
      paragraphs: stories[i.id],
      note: i.id === "atelier" ? "Animology · En conception" : i.chapter,
      tags: [i.short, i.id === "atelier" ? "Animology" : "Parcours"],
    },
  ]),
);
export const dockPosition = (i) => [
  i.position[0] + 7,
  i.position[1],
  i.position[2] + 7,
];
export const berthPosition = (i) => [
  i.position[0] + 13,
  i.position[1] - 1,
  i.position[2] + 6,
];
export const constrainWalker = (x, z, island) => {
  let dx = x - island.position[0],
    dz = z - island.position[2];
  const distance = Math.hypot(dx, dz),
    limit = island.radius - 0.9;
  if (distance > limit) {
    dx *= limit / distance;
    dz *= limit / distance;
  }
  const obstacles = island.id === "circus" ? [[0, -3, 4.5]] : [[-3, -3, 3.4]];
  for (const [ox, oz, radius] of obstacles)
    if (Math.hypot(dx - ox, dz - oz) < radius) {
      const angle = Math.atan2(dz - oz, dx - ox);
      dx = ox + Math.cos(angle) * radius;
      dz = oz + Math.sin(angle) * radius;
    }
  return [dx + island.position[0], dz + island.position[2]];
};
export const nearestIsland = (x, z) =>
  islands.reduce((best, island) => {
    const dock = dockPosition(island),
      distance = Math.hypot(x - dock[0], z - dock[2]);
    return !best || distance < best.distance ? { island, distance } : best;
  }, null);
export const deadZone = (value, threshold = 0.16) =>
  Math.abs(value) < threshold
    ? 0
    : (value - Math.sign(value) * threshold) / (1 - threshold);
