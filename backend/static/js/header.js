(function () {
  function makeMobileMenuBurgerInteractive() {
    // Bulma mobile navbar
    // Get all "navbar-burger" elements
    const navbarBurgers = document.querySelectorAll(".navbar-burger");

    // Add a click event on each of them
    navbarBurgers.forEach((el) => {
      el.addEventListener("click", () => {
        // Get the target from the "data-target" attribute
        const targetId = el.dataset.target;
        const $target = document.getElementById(targetId);

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle("is-active");
        $target.classList.toggle("is-active");
      });
    });
  }

  function makeSearchIconsInteractive() {
    // Search icon in the navbar
    const FOCUSOUTDELAY = 5000;

    const searchNavParentEls = document.querySelectorAll(".title-search");
    for (let searchNav of searchNavParentEls) {
      const searchInput = searchNav.querySelector(".title-search-input");
      const searchForm = searchNav.querySelector(".title-search-form");
      const searchIcon = searchNav.querySelector(".title-search-icon");

      let focusOutTimeout = null;

      function isActive(elem) {
        return document.activeElement == elem;
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
  }

  // place all eventListeners here
  const eventListenersToPlace = [
    makeMobileMenuBurgerInteractive,
    makeSearchIconsInteractive,
  ];

  function runEventListenerPlacements() {
    eventListenersToPlace.forEach((fn) => fn());
  }

  function addListenersOnPageLoadAndAttachToHtmx() {
    runEventListenerPlacements();
    document.body.addEventListener(
      "htmx:historyRestore",
      runEventListenerPlacements
    );
  }

  document.addEventListener(
    "DOMContentLoaded",
    addListenersOnPageLoadAndAttachToHtmx
  );

  // reveal header bar logo on scroll
  let lastKnownScrollPosition = 0;
  let tickingTime = 0;
  const debounceTime = 200;
  const positionThreshold = 120;
  const headerBarLogo = document.getElementById("header-bar-logo");

  function revealHeaderBarLogo(scrollPosition) {
    if (scrollPosition > positionThreshold) {
      headerBarLogo.classList.remove("is-transparent");
    } else {
      headerBarLogo.classList.add("is-transparent");
    }
  }

  document.addEventListener(
    "onscrollend" in document ? "scrollend" : "scroll",
    function (e) {
      // act immediately, then debounce
      if (Date.now() > tickingTime) {
        lastKnownScrollPosition = window.scrollY;
        revealHeaderBarLogo(lastKnownScrollPosition);
        tickingTime = Date.now() + debounceTime;
      }
    }
  );
})();
