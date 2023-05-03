window.addEventListener('load', () => {

    function expandTagsInParentEl() {
        this.parentElement.querySelectorAll(".is-hidden").forEach(elem => elem.classList.remove("is-hidden"));
        this.remove();
    }

    let tagExpanderElems = document.querySelectorAll("a.tag-expander");
    tagExpanderElems.forEach(elem => elem.addEventListener("click", expandTagsInParentEl));

    htmx.onLoad(function (content) {
        content.querySelectorAll("a.tag-expander").forEach(elem => elem.addEventListener("click", expandTagsInParentEl));
    });
});