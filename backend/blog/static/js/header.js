document.addEventListener('DOMContentLoaded', () => {

    // Bulma mobile navbar
    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Add a click event on each of them
    $navbarBurgers.forEach(el => {
        el.addEventListener('click', () => {

            // Get the target from the "data-target" attribute
            const target = el.dataset.target;
            const $target = document.getElementById(target);

            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            el.classList.toggle('is-active');
            $target.classList.toggle('is-active');

        });
    });

    // Search icon in the navbar
    const searchInput = document.getElementById("title-search-input");
    const searchForm = document.getElementById("title-search-form");
    const searchIcon = document.getElementById("title-search-icon");

    function isActive(elem) {
        return (document.activeElement == elem);
    }

    function toggleSearchElemVisibility() {
        searchIcon.classList.toggle("is-hidden");
        searchForm.classList.toggle("is-hidden");
    }

    searchIcon.addEventListener("click", () => {
        toggleSearchElemVisibility();
        searchInput.focus();
    });

    let focusOutTimeout = null;

    searchInput.addEventListener("focusout", () => {
        focusOutTimeout = setTimeout(() => {
            if (!isActive(searchInput)) toggleSearchElemVisibility();
            focusOutTimeout = null;
        }, 5000);

    });

    searchInput.addEventListener("focus", () => {
        if (focusOutTimeout != null) clearTimeout(focusOutTimeout);
    });
});