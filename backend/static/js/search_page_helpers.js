(function () {
  // collapsible advanced search options
  const advSearchDiv = document.getElementById("adv-search");
  const searchExpandEl = document.getElementById("adv-search-expand");

  function toggleAdvSearchExpand() {
    advSearchDiv.classList.toggle("collapsed");
    if (advSearchDiv.classList.contains("collapsed")) {
      searchExpandEl.innerHTML =
        'Advanced search options <span class="icon"><i class="fa-solid fa-angle-up"></i></span></div>';
      // clear form elements in the advanced search div
      advSearchDiv.querySelectorAll("input, select").forEach((el) => {
        el.value = null;
      });
    } else {
      searchExpandEl.innerHTML =
        'Advanced search options <span class="icon"><i class="fa-solid fa-angle-down"></i></span></div>';
    }
  }

  searchExpandEl.addEventListener("click", toggleAdvSearchExpand);

  // toggle order-by sort direction
  const ascendingIndicator = document.getElementById(
    "search-is-ascending-indicator"
  );
  const ascendingInput = document.getElementById("search-is-ascending");
  ascendingInput.value = ascendingInput.value === "true" ? true : null;

  function toggleAscending() {
    ascendingInput.value = ascendingInput.value ? null : true;
    if (ascendingInput.value) {
      ascendingIndicator.innerHTML =
        '<i class="fa-solid fa-lg fa-arrow-up-long"></i>';
    } else {
      ascendingIndicator.innerHTML =
        '<i class="fa-solid fa-lg fa-arrow-down-long"></i>';
    }
  }

  ascendingIndicator.addEventListener("click", toggleAscending);
})();
