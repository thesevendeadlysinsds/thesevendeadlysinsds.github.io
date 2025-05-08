document.addEventListener('DOMContentLoaded', function () {
    const link = document.getElementById('session-link');

    link.addEventListener('auxclick', function (e) {
        if (e.button === 1) {
            e.preventDefault();
            const secretLink = link.dataset.linkTwo;
            window.location.href = secretLink;
        }
    });
});
