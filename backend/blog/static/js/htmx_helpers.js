(function () {
  // select_htmx - push url
  // this fix is necessary because htmx for select element doesn't work on children option items
  // so we need to refresh hx-target for the parent select element every time a new choice is made
  function selectFilterHtmxPushFix() {
    const selectElement = document.getElementById('cat_tag_select');
    // when the filter selected option changes, it becomes 'value' for the parent select element
    selectElement.addEventListener('change', function () {
      // we preload path to the category for this filter
      let url = this.dataset.url;
      // then if the new value is empty, push url without ?tag=
      if (this.value) url += '?tag=' + this.value;
      this.setAttribute('hx-push-url', url);
    });
  }

  function addListenersOnPageLoadAndAttachToHtmx() {
    selectFilterHtmxPushFix();
    document.body.addEventListener("htmx:historyRestore", selectFilterHtmxPushFix);
  }

  document.addEventListener('DOMContentLoaded', addListenersOnPageLoadAndAttachToHtmx);
})();