(function () {
    // when there are too many tags in a post, expand them using a 'Show all' button
    function expandTagsInParentEl() {
        this.parentElement.querySelectorAll(".is-hidden").forEach(elem => elem.classList.remove("is-hidden"));
        this.remove();
    }

    function addListenersOnPageLoadAndAttachToHtmx() {
        const tagExpanderElems = document.querySelectorAll("a.tag-expander");
        tagExpanderElems.forEach(elem => elem.addEventListener("click", expandTagsInParentEl));

        htmx.onLoad(function (content) {
            content.querySelectorAll("a.tag-expander").forEach(elem => elem.addEventListener("click", expandTagsInParentEl));
        });
    }

    document.addEventListener('DOMContentLoaded', addListenersOnPageLoadAndAttachToHtmx);
})();