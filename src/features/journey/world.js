export const islands = [
  { id: 'atelier', name: 'Le port des possibles', chapter: 'Création numérique', position: [0, 0, 0], radius: 12, color: '#e7b75b', icon: '✦', short: 'L’atelier', description: 'Un port d’attache pour les idées, le code et les projets qui prennent forme.' },
  { id: 'backroads', name: 'L’appel du voyage', chapter: 'Backroads · Expérience professionnelle', position: [-37, 3, -32], radius: 10, color: '#8eb788', icon: '↗', short: 'Backroads', description: 'Une escale dédiée à Backroads dans mon parcours professionnel. Le récit détaillé de cette expérience viendra enrichir ce paysage.' },
  { id: 'theatre', name: 'La vie en mouvement', chapter: 'Cirque & parcours', position: [30, 5, -39], radius: 11, color: '#cf786b', icon: '◒', short: 'Le théâtre', description: 'Des métiers manuels au trapèze, du cirque au développement : un parcours fait de mouvements, d’apprentissage et de création.' },
];

export const exhibits = {
  atelier: { title: 'L’atelier des idées', label: 'Création numérique', paragraphs: ['Le développement web comme nouveau terrain de création, après un parcours entre métiers manuels, agriculture et arts du cirque.', 'Animology est un projet d’encyclopédie animale pour les enfants, imaginé pour une tablette Android. Dinosaures, fiches et exploration visuelle sont au cœur de sa conception.'], note: 'Animology · En conception', tags: ['Web', '3D', 'Expérimentation'] },
  backroads: { title: 'Backroads', label: 'Expérience professionnelle', paragraphs: ['Backroads a sa place dans mon parcours professionnel. Cette île lui est consacrée.', 'Le décor évoque le voyage. Les fonctions, les dates et les anecdotes seront ajoutées à partir du récit de cette expérience.'], note: 'Récit de l’escale à venir', tags: ['Parcours', 'Voyage'] },
  theatre: { title: 'La vie en mouvement', label: 'Du geste au code', paragraphs: ['Entrepôt, maçonnerie, agriculture, trapèze au Club Med, puis dix années de cirque : plusieurs univers, un même goût pour apprendre en faisant.', 'L’apprentissage en autodidacte et la formation O’Clock ouvrent ensuite un nouveau chapitre : le développement.'], note: 'Un parcours à explorer', tags: ['Savoir-faire', 'Cirque', 'Développement'] },
};

/** Return the boarding point shared by navigation and scenery. */
export const dockPosition = (island) => [island.position[0] + 6, island.position[1], island.position[2] + 5];

/** Keep the walker on the current island and outside solid scenery. */
export const constrainWalker = (x, z, island) => {
  let dx = x - island.position[0];
  let dz = z - island.position[2];
  const distance = Math.hypot(dx, dz);
  const limit = island.radius - 0.9;
  if (distance > limit) { dx *= limit / distance; dz *= limit / distance; }
  // Buildings and the tent occupy the rear of each island.
  const obstacles = island.id === 'atelier' ? [[-3, -3, 3.4]] : island.id === 'theatre' ? [[0, -3, 4]] : [[-3, -3, 2.8]];
  for (const [ox, oz, radius] of obstacles) {
    const distanceToObstacle = Math.hypot(dx - ox, dz - oz);
    if (distanceToObstacle < radius) {
      const angle = Math.atan2(dz - oz, dx - ox);
      dx = ox + Math.cos(angle) * radius;
      dz = oz + Math.sin(angle) * radius;
    }
  }
  return [dx + island.position[0], dz + island.position[2]];
};

/** Choose the nearest safe harbour using horizontal distance. */
export const nearestIsland = (x, z) => islands.reduce((best, island) => {
  const dock = dockPosition(island);
  const distance = Math.hypot(x - dock[0], z - dock[2]);
  return !best || distance < best.distance ? { island, distance } : best;
}, null);

/** Apply a radial dead zone to analog input. */
export const deadZone = (value, threshold = 0.16) => Math.abs(value) < threshold ? 0 : (value - Math.sign(value) * threshold) / (1 - threshold);
