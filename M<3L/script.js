let currentLetter = 'M';
const letterElement = document.getElementById('animatedLetter');

function changeLetter() {
    if (currentLetter === 'M') {
        currentLetter = '<3';
        letterElement.style.color = 'darkred';
    } else if (currentLetter === '<3') {
        currentLetter = 'L';
        letterElement.style.color = 'darkgray';
    } else {
        currentLetter = 'M';
        letterElement.style.color = 'darkgray';
    }
    letterElement.textContent = currentLetter;
}

letterElement.addEventListener('animationiteration', changeLetter);

// Initial rotation
letterElement.classList.add('rotating');
