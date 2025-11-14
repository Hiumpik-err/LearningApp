document.addEventListener('DOMContentLoaded', function() {
    const readMoreButtons = document.querySelectorAll('.read-more');
    const overlayContent = document.getElementById('overlay-content');
    const overlay = document.getElementById('overlay-card');
    const overlayTitle = document.getElementById('overlay-title');
    function showArticle(title, content) {
        content = content.replace(/\\u0027/g, "'");
        const jsonString = content.replace(/'/g, '"').trim();

        let parsed;
        try {
            parsed = JSON.parse(jsonString);
        } catch (e) {
            console.error("Failed to parse article JSON:", e);
            return;
        }

        // Step 2: fill overlay content
        overlayTitle.textContent = title;
        overlayContent.innerHTML = '';

        parsed.headers.forEach((header, i) => {
            const h = document.createElement('h4');
            h.classList.add('section-header');
            h.textContent = header;

            const p = document.createElement('p');
            p.textContent = parsed.contents[i] || '';

            overlayContent.appendChild(h);
            overlayContent.appendChild(p);
        });
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