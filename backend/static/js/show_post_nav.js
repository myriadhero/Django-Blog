"use strict";
(function () {
  const STICKIES_OFFSET = 160;
  const HEADING_SCROLL_THRESHOLD = 255;
  const SCROLL_DEBOUNCE_MS = 50;

  function createIdFromText(text) {
    let newId = text
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, "") // Remove special characters
      .trim()
      .replace(/\s+/g, "-") // Replace spaces with hyphens
      .replace(/-+/g, "-"); // Replace multiple hyphens with single

    let fill = 0;
    let tempId = newId || "section";
    while (document.getElementById(tempId)) {
      fill += 1;
      tempId = `${newId}-${fill}`;
    }
    return tempId;
  }

  function scrollToTargetElem(targetElem) {
    const targetPosition =
      targetElem.getBoundingClientRect().top + window.scrollY - STICKIES_OFFSET;
    window.scrollTo({ top: targetPosition, behavior: "smooth" });
  }

  function scrollEvtListener(e) {
    e.preventDefault();
    const targetSection = document.getElementById(e.target.href.split("#")[1]);
    history.replaceState(null, "", e.target.href);
    scrollToTargetElem(targetSection);
  }

  function convertToLinkHeading(headingElem) {
    const link = document.createElement("a");
    if (!headingElem.id) {
      headingElem.id = createIdFromText(headingElem.textContent);
    }
    link.href = `#${headingElem.id}`;
    link.classList.add("is-link-black");
    link.textContent = headingElem.textContent;
    headingElem.innerHTML = "";
    headingElem.appendChild(link);
    link.addEventListener("click", scrollEvtListener);
  }

  function createNavBar() {
    const postContent = document.getElementById("post-content");
    const navBar = document.getElementById("post-nav");

    const allHeadings = postContent.querySelectorAll("h1, h2, h3, h4");
    const h1headings = postContent.querySelectorAll("h1");
    const navLinks = [];

    allHeadings.forEach((heading) => {
      convertToLinkHeading(heading);
    });

    if (h1headings.length === 0) {
      navBar.style.display = "none";
      return;
    }

    // Create navigation links for each H1 heading
    h1headings.forEach((heading) => {
      const navLink = document.createElement("a");
      navLink.textContent = heading.textContent;
      navLink.href = `#${heading.id}`;
      navLink.dataset.targetId = heading.id;

      navLink.addEventListener("click", scrollEvtListener);

      navBar.appendChild(navLink);
      navLinks.push(navLink);
    });

    navBar.classList.remove("is-invisible");

    // Check if there's a hash in the URL and scroll to the section
    if (window.location.hash) {
      const targetId = window.location.hash.substring(1); // Remove the '#' from hash
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        scrollToTargetElem(targetSection);
      }
    }

    let lastScrolledLinkId = null;
    let debouncedEvt = null;
    // Function to update the active nav link based on scroll position
    function updateActiveNavLink() {
      if (debouncedEvt != null) {
        return;
      }
      debouncedEvt = setTimeout((event) => {
        let currentSectionId = null;
        if (
          h1headings[0].getBoundingClientRect().top < HEADING_SCROLL_THRESHOLD
        ) {
          // Find the closest heading to the top of the viewport
          for (const heading of h1headings) {
            const rect = heading.getBoundingClientRect();
            // If the heading's top is in or above the viewport, it's the active section
            if (rect.top <= HEADING_SCROLL_THRESHOLD) {
              currentSectionId = heading.id;
            }
            // If we've passed the last heading, keep the last one active
            else {
              break; // Stop once we find the first heading below the viewport
            }
          }
        } else {
          // If we are above all headings, scroll the navbar to start
          navBar.children[0].scrollIntoView({
            inline: "center",
            behavior: "smooth",
            block: "nearest",
          });
        }

        // Update the active class on nav links
        navLinks.forEach((link) => {
          if (link.dataset.targetId === currentSectionId) {
            link.classList.add("active");

            if (
              lastScrolledLinkId !== currentSectionId &&
              link.getBoundingClientRect().top > 0
            ) {
              link.scrollIntoView({
                inline: "center",
                behavior: "smooth",
                block: "nearest",
              });
              lastScrolledLinkId = currentSectionId;
            }
          } else {
            link.classList.remove("active");
          }
        });
        debouncedEvt = null;
      }, SCROLL_DEBOUNCE_MS);
    }

    // Update active nav link on scroll
    window.addEventListener("scrollend", updateActiveNavLink);
  }

  // Run the function when the page loads
  window.onload = createNavBar;
})();
