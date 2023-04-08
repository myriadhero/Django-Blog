// select_htmx
document.addEventListener('DOMContentLoaded', function () {
  // onchange="this.setAttribute('hx-push-url', '{{ category.get_absolute_url }}' + (this.value !== '' ? ('?tag=' + this.value) : ''));"
  const selectElement = document.getElementById('cat_tag_select');
  if (selectElement) {
    selectElement.addEventListener('change', function () {
      let url = this.dataset.url;
      if (this.value) url += '?tag=' + this.value;
      this.setAttribute('hx-push-url', url);
    });
  }
});