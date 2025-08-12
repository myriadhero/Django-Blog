(function () {
  const stickiesOffset = 160;
  const headingScrollThreshold = 255;
  const scrollDebounceMs = 50;

  function createIdFromText(text) {
    let newId = text
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, "") // Remove special characters
      .trim()
      .replace(/\s+/g, "-") // Replace spaces with hyphens
      .replace(/-+/g, "-"); // Replace multiple hyphens with single

    if (!newId) {
      newId = `section-${index + 1}`;
    }

    let fill = 0;
    let tempId = newId;
    while (document.getElementById(tempId)) {
      fill += 1;
      tempId = `${newId}-${fill}`;
    }
    return tempId;
  }

  function scrollToTargetElem(targetElem) {
    const targetPosition =
      targetElem.getBoundingClientRect().top + window.scrollY - stickiesOffset;
    window.scrollTo({ top: targetPosition, behavior: "smooth" });
  }

  function createNavBar() {
    // get every H1
    // make a little nav bar that links directly to those items
    // nav bar should by default be collapsed
    const postContent = document.getElementById("post-content");
    const navBar = document.getElementById("post-nav");

    // Find all H1 headings
    const headings = postContent.querySelectorAll("h1");
    const navLinks = [];
    let lastScrolledLinkId = null;

    // Create navigation links for each H1 heading
    headings.forEach((heading, index) => {
      // Create an ID based on the heading's text content
      const headingId = createIdFromText(heading.textContent, index);
      heading.id = headingId;

      // Create a nav link
      const navLink = document.createElement("a");
      navLink.textContent = heading.textContent;
      navLink.href = `#${headingId}`;
      navLink.dataset.targetId = headingId;

      // Add click event to scroll smoothly
      navLink.addEventListener("click", (e) => {
        e.preventDefault();
        const targetSection = document.getElementById(headingId);
        history.replaceState(null, "", `#${headingId}`);
        scrollToTargetElem(targetSection);
      });

      // Append the link to the nav bar
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

    let debounce = null;
    // Function to update the active nav link based on scroll position
    function updateActiveNavLink() {
      if (debounce != null) {
        return;
      }
      debounce = setTimeout((event) => {
        if (headings[0].getBoundingClientRect().top < headingScrollThreshold) {
          // Find the closest heading to the top of the viewport
          for (const heading of headings) {
            const rect = heading.getBoundingClientRect();
            // If the heading's top is in or above the viewport, it's the active section
            if (rect.top <= headingScrollThreshold) {
              currentSectionId = heading.id;
            }
            // If we've passed the last heading, keep the last one active
            else {
              break; // Stop once we find the first heading below the viewport
            }
          }
        } else {
          currentSectionId = null;
          lastScrolledLinkId = null;
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
              lastScrolledLinkId !== link.dataset.targetId &&
              link.getBoundingClientRect().top > 0
            ) {
              link.scrollIntoView({
                inline: "center",
                behavior: "smooth",
                block: "nearest",
              });
              lastScrolledLinkId = link.dataset.targetId;
            }
          } else {
            link.classList.remove("active");
          }
        });
        debounce = null;
      }, scrollDebounceMs);
    }

    // Update active nav link on scroll
    window.addEventListener("scrollend", updateActiveNavLink);
  }

  // Run the function when the page loads
  window.onload = createNavBar;
})();
