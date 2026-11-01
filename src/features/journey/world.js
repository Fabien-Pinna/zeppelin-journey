/** Physical chapters and narrative share one source, including the text edition. */
import { landscapes } from './landscape.js';
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
    [46, 4, -22],
    "#86babc",
    "⌁",
  ],
  [
    "circus",
    "Les années cirque",
    "Dix ans de piste et de coulisses",
    "Bouglione · 10 années",
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
  radius: Math.max(landscapes[id].rx, landscapes[id].rz) * 1.15,
  landscape: landscapes[id],
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
    "J’ai travaillé dans les vignes, les cerisiers et les oliviers du Vaucluse, au pied du mont Ventoux.",
    "Les rangs de vigne, le verger et l’oliveraie donnent à cette escale son paysage provençal, entre terres cultivées et pierres claires.",
  ],
  clubmed: [
    "J’ai travaillé au Club Med de Gregolimano, sur l’île d’Eubée en Grèce, et à Beldi, près d’Antalya en Turquie.",
    "Plages, ski nautique, cours de voile, trapèze volant, piscines et spectacles au théâtre de plein air : cette île rassemble les souvenirs de ces deux villages méditerranéens.",
  ],
  circus: [
    "Dix années avec Bouglione, en tournée sous chapiteau et pour les spectacles du Cirque d’Hiver à Paris.",
    "Assistant régisseur, garçon de piste, monteur de chapiteau : je travaillais aussi à l’affichage publicitaire et au camion d’annonce du spectacle. Les artistes, les animaux et les caravanes évoquent cet univers, côté piste et côté coulisses.",
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
export { moveWalker } from "./physics.js";
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
