let counter = 0;
const counterDisplay = document.getElementById('counter');
const incrementBtn = document.getElementById('increment');
const decrementBtn = document.getElementById('decrement');

function updateCounter() {
    counterDisplay.textContent = counter;
}

incrementBtn.addEventListener('click', () => {
    counter++;
    updateCounter();
});

decrementBtn.addEventListener('click', () => {
    counter--;
    updateCounter();
});

console.log('Flask project loaded!');