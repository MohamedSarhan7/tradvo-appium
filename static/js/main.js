function increaseFontSize() {
  document.body.style.fontSize =
    parseFloat(getComputedStyle(document.body).fontSize) * 1.1 + 'px';

    console.log("increased font size")
}


function decreaseFontSize() {
  document.body.style.fontSize =
    parseFloat(getComputedStyle(document.body).fontSize) * 0.9 + 'px';
}
function toggleHighContrast() {
  document.body.classList.toggle('high-contrast');
}