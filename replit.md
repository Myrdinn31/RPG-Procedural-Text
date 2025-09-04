# Overview

Un projet web interactif simple construit avec HTML, CSS et JavaScript vanilla. Le projet présente un compteur interactif et des cartes d'information animées. Il démontre un développement web propre, sans frameworks, avec un design moderne et des effets glassmorphism.

# User Preferences

Style de communication préféré: Langage simple et quotidien.

# System Architecture

## Structure du Projet
```
/
├── index.html    # Page principale HTML
├── style.css     # Feuille de style CSS
├── script.js     # Logique JavaScript
└── replit.md     # Documentation du projet
```

## Architecture Frontend
- **Technologies Web Vanilla**: Construit entièrement avec HTML5, CSS3, et JavaScript ES6 sans frameworks
- **Application Page Unique**: Structure HTML statique avec interactivité JavaScript
- **Pensée Composants**: Sections modulaires (compteur, cartes info) facilement extensibles
- **Programmation Événementielle**: Utilise des écouteurs d'événements DOM pour les interactions

## Design Patterns
- **Séparation des Préoccupations**: Séparation claire entre structure (HTML), présentation (CSS), et comportement (JavaScript)
- **Amélioration Progressive**: Fonctionnalité de base sans JavaScript, améliorée avec animations et interactivité
- **Design Responsive**: Approche mobile-first avec layouts flexibles

## Architecture CSS
- **Fonctionnalités CSS Modernes**: Utilise flexbox, CSS Grid, backdrop-filter pour les effets glassmorphism
- **Système d'Animation**: Transitions CSS combinées avec animations déclenchées par JavaScript
- **Arrière-plans Dégradés**: Dégradés linéaires pour l'attrait visuel
- **Design Responsive**: Media queries pour l'adaptation mobile

## Architecture JavaScript
- **Manipulation DOM**: Accès et manipulation directe du DOM pour mises à jour en temps réel
- **Coordination d'Animation**: Animations CSS et JavaScript coordonnées pour une expérience fluide
- **Gestion d'Événements**: Écouteurs d'événements pour l'interactivité utilisateur

# Fonctionnalités

## Compteur Interactif
- Boutons d'incrémentation et décrémentation
- Animation lors des changements de valeur
- Design moderne avec effets de survol

## Cartes d'Information
- Trois cartes présentant les avantages du projet
- Effets de survol avec transformations
- Animation d'entrée échelonnée

## Fonctionnalités Bonus
- Double-clic sur le titre change la couleur de fond
- Animations fluides et feedback visuel

# External Dependencies

## Runtime Dependencies
- **Aucune**: L'application fonctionne entièrement avec des technologies web vanilla

## Browser APIs
- **DOM API**: Pour la sélection et manipulation d'éléments
- **Event API**: Pour la gestion des interactions utilisateur
- **CSS Transitions**: Pour les animations fluides et feedback visuel

## Development Environment
- **Serveur de Fichiers Statiques**: Python HTTP server sur port 5000
- **Navigateur Moderne**: Nécessite support ES6+ pour arrow functions et CSS moderne