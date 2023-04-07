document.addEventListener('DOMContentLoaded', function () {
    const tagInputs = document.querySelectorAll('[data-autocomplete-url]');
  
    // Iterate through all the elements with the data-autocomplete-url attribute
    tagInputs.forEach((tagInput) => {
      const autocompleteUrl = tagInput.dataset.autocompleteUrl;
      // Your autocomplete logic goes here, using the `autocompleteUrl` variable for each element
    });
  });

document.addEventListener('DOMContentLoaded', function () {
    const tagInput = document.querySelector('.taggit-tags');
    const suggestionsList = document.createElement('ul');
    suggestionsList.className = 'suggestions';
    tagInput.parentNode.appendChild(suggestionsList);
  
    function split(val) {
      return val.split(/,\s*/);
    }
  
    function extractLast(term) {
      return split(term).pop();
    }
  
    async function fetchTags(term) {
      const response = await fetch(`/tags/autocomplete/?term=${term}`);
      const data = await response.json();
      return data.map((item) => item.value);
    }
  
    function showSuggestions(tags) {
      suggestionsList.innerHTML = '';
      tags.forEach((tag) => {
        const listItem = document.createElement('li');
        listItem.textContent = tag;
        listItem.addEventListener('click', () => {
          selectTag(tag);
        });
        suggestionsList.appendChild(listItem);
      });
    }
  
    function hideSuggestions() {
      suggestionsList.innerHTML = '';
    }
  
    function selectTag(tag) {
      const terms = split(tagInput.value);
      terms.pop();
      terms.push(tag);
      terms.push('');
      tagInput.value = terms.join(', ');
      hideSuggestions();
    }
  
    tagInput.addEventListener('input', async () => {
      const term = extractLast(tagInput.value);
      if (term.length < 1) {
        hideSuggestions();
        return;
      }
      const tags = await fetchTags(term);
      showSuggestions(tags);
    });
  
    tagInput.addEventListener('blur', () => {
      setTimeout(hideSuggestions, 150);
    });
  });
  