// Variables
let counter = 0;

// Éléments DOM
const counterDisplay = document.getElementById('counter');
const incrementBtn = document.getElementById('increment');
const decrementBtn = document.getElementById('decrement');

// Fonction pour mettre à jour l'affichage
function updateCounter() {
    counterDisplay.textContent = counter;
    
    // Animation simple lors du changement
    counterDisplay.style.transform = 'scale(1.2)';
    setTimeout(() => {
        counterDisplay.style.transform = 'scale(1)';
    }, 150);
}

// Gestionnaires d'événements
incrementBtn.addEventListener('click', () => {
    counter++;
    updateCounter();
});

decrementBtn.addEventListener('click', () => {
    counter--;
    updateCounter();
});

// Animation d'entrée au chargement
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Projet simple chargé avec succès !');
    
    // Animation d'entrée pour les cartes
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 800 + (index * 200));
    });
});

// Fonctionnalité bonus: changement de couleur au clic
function changeBackgroundColor() {
    const colors = [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
    ];
    
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    document.body.style.background = randomColor;
}

// Ajout d'un événement au double-clic sur le titre
document.querySelector('h1').addEventListener('dblclick', () => {
    changeBackgroundColor();
    console.log('🎨 Couleur de fond changée !');
});