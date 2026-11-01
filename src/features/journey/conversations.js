export const conversations = {
  atelier: {
    name: "Le créateur",
    role: "À l’atelier",
    greeting:
      "Bienvenue au port des possibles. Ici, le voyage continue à travers le développement et les projets numériques.",
    topics: [
      [
        "Que crée Fabien aujourd’hui ?",
        "Le développement web est un nouveau terrain de création dans son parcours, après les métiers de terrain et les arts du cirque. Cet archipel en est une manière de raconter les étapes.",
      ],
      [
        "Parle-moi d’Animology.",
        "Animology est une encyclopédie animale pour les enfants, pensée pour une tablette Android. Dinosaures, fiches et exploration visuelle : le projet est encore en conception.",
      ],
      [
        "Où commence le voyage ?",
        "L’entrepôt, la maçonnerie et l’agriculture ont aussi leur place dans cette histoire. Chaque île raconte un chapitre : prends le temps de les explorer.",
      ],
    ],
  },
  warehouse: {
    name: "Le magasinier",
    role: "À l’entrepôt",
    greeting:
      "Attention au passage des caisses ! Cette escale raconte l’expérience de Fabien en entrepôt, l’un de ses métiers de terrain.",
    topics: [
      [
        "Pourquoi cette escale ?",
        "Avant le développement, le parcours de Fabien passe aussi par le travail en entrepôt. Cette expérience mérite son propre chapitre, à côté des autres métiers.",
      ],
      [
        "Que se passe-t-il ici ?",
        "Le porteur fait sa tournée entre les piles de caisses. Le chariot et les palettes évoquent cet univers de manutention. Le décor est une évocation, pas la reproduction d’un employeur précis.",
      ],
      [
        "Et la suite ?",
        "Continue vers la maçonnerie : on y passe des caisses aux matériaux et à la construction.",
      ],
    ],
  },
  masonry: {
    name: "Le tailleur de pierre",
    role: "Au chantier",
    greeting:
      "Approche. Ici, l’histoire se construit pierre après pierre : la maçonnerie fait partie du parcours professionnel de Fabien.",
    topics: [
      [
        "Avant les lignes de code ?",
        "Oui, il y a eu le travail manuel et la maçonnerie. Construire avec des matériaux appartient à son parcours, avant la création numérique.",
      ],
      [
        "Que regardes-tu ?",
        "L’arche, les pierres et les outils donnent une forme à ce chapitre. Regarde le geste du tailleur près du petit stock de pierres.",
      ],
      [
        "Quelle autre escale visiter ?",
        "L’agriculture raconte un autre métier de terrain, dans un tout autre rythme.",
      ],
    ],
  },
  farm: {
    name: "Le jardinier",
    role: "À la ferme",
    greeting:
      "Bienvenue au rythme du vivant. Le travail agricole fait lui aussi partie du parcours de Fabien.",
    topics: [
      [
        "Quelle place dans son parcours ?",
        "L’agriculture est l’une de ses expériences professionnelles, au même titre que l’entrepôt et la maçonnerie. Elle a donc son île à part entière.",
      ],
      [
        "Un détail à observer ?",
        "Les ailes du moulin tournent, les moutons remuent près des cultures et le jardinier prend soin du potager. Ce petit paysage évoque le travail agricole.",
      ],
      [
        "On prend de la hauteur ?",
        "L’escale du Club Med t’attend : cette fois, le mouvement se poursuit au trapèze.",
      ],
    ],
  },
  clubmed: {
    name: "Le trapéziste",
    role: "Au pied du portique",
    greeting:
      "Lève les yeux : quelqu’un est déjà en piste ! Le trapèze au Club Med marque une étape du parcours de Fabien dans les airs.",
    topics: [
      [
        "C’est le début du cirque ?",
        "Cette étape au Club Med précède le long chapitre consacré au cirque. Le trapèze est le cœur de cette escale.",
      ],
      [
        "Comment observer le mouvement ?",
        "Regarde les mains sur la barre, puis le passage au-dessus du filet. Tu peux rapprocher la caméra avec le zoom et tourner autour du portique.",
      ],
      [
        "Combien de temps dans le cirque ?",
        "La prochaine île raconte dix années de cirque : un chapitre à part entière.",
      ],
    ],
  },
  circus: {
    name: "Le régisseur",
    role: "Sous le chapiteau",
    greeting:
      "Bienvenue dans les années cirque. Dix années du parcours de Fabien sont consacrées à cet univers.",
    topics: [
      [
        "Dix ans ?",
        "Oui. Après le trapèze au Club Med, les arts du cirque occupent dix années de son parcours. Le chapiteau représente ce chapitre.",
      ],
      [
        "Le spectacle a commencé ?",
        "Le jongleur répète sur la piste. Ses balles suivent leur trajectoire entre deux lancers, tandis que les gradins attendent les visiteurs.",
      ],
      [
        "Et après la piste ?",
        "L’apprentissage en autodidacte puis la formation O’Clock font partie du chemin vers le développement.",
      ],
    ],
  },
  backroads: {
    name: "Le mécanicien",
    role: "À la maison d’étape",
    greeting:
      "Bienvenue chez Backroads. Cette expérience professionnelle a aussi sa place dans le voyage de Fabien.",
    topics: [
      [
        "Quel chapitre est-ce ?",
        "Backroads fait partie de son parcours professionnel. Les vélos, le fourgon et la maison d’étape évoquent ici l’univers du voyage.",
      ],
      [
        "Que prépare le mécanicien ?",
        "Il vérifie un vélo avant le départ. Cette scène anime l’escale ; elle ne prétend pas décrire le poste exact occupé par Fabien.",
      ],
      [
        "Où se situe cette étape ?",
        "La carte est un archipel à explorer librement. La position de Backroads n’indique pas une date ou un ordre chronologique précis.",
      ],
    ],
  },
  learning: {
    name: "Le lecteur",
    role: "Au coin des livres",
    greeting:
      "Un livre ouvert, une question, puis une autre… L’apprentissage en autodidacte ouvre ici la voie à la création numérique.",
    topics: [
      [
        "Apprendre par soi-même ?",
        "Cette phase d’apprentissage personnel fait partie du chemin de Fabien vers le développement. Les livres et l’ordinateur en sont les repères dans cette île.",
      ],
      [
        "Que trouve-t-on dans cet atelier ?",
        "Un lieu pour lire, explorer et essayer. Le lecteur feuillette son carnet, entouré de livres et d’un poste de travail.",
      ],
      [
        "Quelle est l’étape suivante ?",
        "La formation O’Clock prolonge cet apprentissage personnel. Son école se trouve sur une autre île.",
      ],
    ],
  },
  oclock: {
    name: "Le formateur",
    role: "À l’école O’Clock",
    greeting:
      "Bienvenue à O’Clock. Cette formation constitue une étape du parcours de Fabien vers le développement.",
    topics: [
      [
        "Après l’autodidacte ?",
        "La formation O’Clock prolonge l’apprentissage personnel. Cette escale marque ce passage vers le développement.",
      ],
      [
        "Que se passe-t-il dans la classe ?",
        "Le formateur montre le tableau, l’horloge avance et les postes attendent les élèves. Le décor évoque un atelier collectif d’apprentissage.",
      ],
      [
        "Et maintenant ?",
        "Retour au port des possibles : le développement et les projets numériques y prennent le relais, dont Animology, encore en conception.",
      ],
    ],
  },
};
