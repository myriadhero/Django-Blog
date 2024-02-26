(function () {
  const DELAY = 200;
  const tagQuickSearch = document.getElementById("tag-quick-search");
  const tagLinks = document.querySelectorAll(".tag-name");
  const allTagsElem = document.getElementById("all-tags");
  let timerId = null;

  function filterTags() {
    const query = tagQuickSearch.value.toLowerCase().replaceAll(" ", "");

    if (query == "") {
      allTagsElem.classList.remove("searched");
      for (const tagLink of tagLinks) {
        tagLink.classList.remove("searched");
      }
      return;
    }

    allTagsElem.classList.add("searched");

    for (const tagLink of tagLinks) {
      const tagName = tagLink.textContent.toLowerCase().replaceAll(" ", "");
      if (tagName.includes(query)) {
        tagLink.classList.add("searched");
      } else {
        tagLink.classList.remove("searched");
      }
    }
  }

  function filterTagsWithTimeout() {
    if (timerId) {
      clearTimeout(timerId);
    }

    timerId = setTimeout(() => {
      timerId = null;
      filterTags();
    }, DELAY);
  }

  document
    .querySelector("#tag-quick-search + .icon")
    .addEventListener("click", () => {
      tagQuickSearch.value = "";
      filterTags();
    });
  tagQuickSearch.addEventListener("input", filterTagsWithTimeout);
})();
