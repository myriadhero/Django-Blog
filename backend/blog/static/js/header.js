(function () {
    function makeMobileMenuBurgerInteractive() {
        // Bulma mobile navbar
        // Get all "navbar-burger" elements
        const navbarBurgers = document.querySelectorAll('.navbar-burger');

        // Add a click event on each of them
        navbarBurgers.forEach(el => {
            el.addEventListener('click', () => {
                // Get the target from the "data-target" attribute
                const targetId = el.dataset.target;
                const $target = document.getElementById(targetId);

                // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                el.classList.toggle('is-active');
                $target.classList.toggle('is-active');
            });
        });
    }

    function makeSearchIconInteractive() {
        // Search icon in the navbar
        const searchInput = document.getElementById("title-search-input");
        const searchForm = document.getElementById("title-search-form");
        const searchIcon = document.getElementById("title-search-icon");
        const searchNav = document.getElementById("title-search");

        const FOCUSOUTDELAY = 5000;
        let focusOutTimeout = null;

        function isActive(elem) {
            return (document.activeElement == elem);
        }

        function toggleSearchElemVisibility() {
            searchIcon.classList.toggle("is-hidden");
            searchForm.classList.toggle("is-hidden");
        }

        function revealFormOnClick() {
            toggleSearchElemVisibility();
            searchInput.focus();
            searchNav.removeEventListener("click", revealFormOnClick);
        }

        function hideFormOnFocusOut() {
            if (!isActive(searchInput)) {
                toggleSearchElemVisibility();
                focusOutTimeout = null;
                searchNav.addEventListener("click", revealFormOnClick);
            }
        }

        function resetFocusOutTimeoutOnFocus() {
            if (focusOutTimeout != null) {
                clearTimeout(focusOutTimeout);
                focusOutTimeout = null;
            }
        }

        searchNav.addEventListener("click", revealFormOnClick);
        searchInput.addEventListener("focusout", () => {
            focusOutTimeout = setTimeout(hideFormOnFocusOut, FOCUSOUTDELAY);
        });
        searchInput.addEventListener("focus", resetFocusOutTimeoutOnFocus);
    }

    // place all eventListeners here
    const eventListenersToPlace = [
        makeMobileMenuBurgerInteractive,
        makeSearchIconInteractive,
    ];

    function runEventListenerPlacements() {
        eventListenersToPlace.forEach(fn => fn());
    }

    function addListenersOnPageLoadAndAttachToHtmx() {
        runEventListenerPlacements();
        document.body.addEventListener("htmx:historyRestore", runEventListenerPlacements);
    }


    document.addEventListener("DOMContentLoaded", addListenersOnPageLoadAndAttachToHtmx);
})();