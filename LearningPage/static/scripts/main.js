document.addEventListener('DOMContentLoaded', function() {
    const readMoreButtons = document.querySelectorAll('.read-more');
    const overlayContent = document.getElementById('overlay-content');
    const overlay = document.getElementById('overlay-card');
    const overlayTitle = document.getElementById('overlay-title');
    
    function decodeUnicodeEscapes(str) {        
        return str.replace(/\\u([0-9a-fA-F]{4})/g, function(match, code) {
            return String.fromCharCode(parseInt(code, 16));
        });
    }
    
    function showArticle(title, content) {
        overlayTitle.textContent = title;        
        const decodedContent = decodeUnicodeEscapes(content);
        overlayContent.innerHTML = decodedContent;
        overlay.classList.remove('d-none');
    }

    readMoreButtons.forEach(button => {
        button.addEventListener('click', () => {
            showArticle(button.getAttribute('data-title'), button.getAttribute('data-content'));
        });
    });
    const closeOverlayButton = document.getElementById('close-overlay');
    closeOverlayButton.addEventListener('click', () => {
        overlayContent.innerHTML = '';
        overlay.classList.add('d-none');
        readMoreButtons.classList.remove('disabled');
    });
});