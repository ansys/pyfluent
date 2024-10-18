// Global search options
src = "https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js";

// Configure RequireJS
require.config({
  paths: {
    fuse: "https://cdn.jsdelivr.net/npm/fuse.js@6.4.6/dist/fuse.min",
  },
});

// Main script for search functionality
require(["fuse"], function (Fuse) {
  let fuseInstance;
  let searchData = [];
  let currentIndex = -1;

  function initializeFuse(data) {
    const fuseOptions = theme_static_search;
    fuseInstance = new Fuse(data, fuseOptions);
    searchData = data;
  }

  function performSearch(query) {
    const results = fuseInstance.search(query, {
      limit: parseInt(theme_limit),
    });
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = "";
    currentIndex = -1;

    if (results.length === 0) {
      displayNoResultsMessage(resultsContainer);
      return;
    }

    if (query === "") {
      resultsContainer.style.display = "none";
      return;
    }
    resultsContainer.style.display = "block";

    results.forEach((result) => {
      const { title, text, href } = result.item;
      const item = createResultItem(title, text, href, query);
      resultsContainer.appendChild(item);
    });
  }

  function displayNoResultsMessage(container) {
    const noResultsMessage = document.createElement("div");
    noResultsMessage.className = "no-results";
    noResultsMessage.textContent = "No matched documents";
    container.appendChild(noResultsMessage);
  }

  function createResultItem(title, text, href, query) {
    const item = document.createElement("div");
    item.className = "result-item";

    const highlightedTitle = highlightTerms(title, query);
    const highlightedText = highlightTerms(text, query);

    item.innerHTML = `
      <div class="result-title">${highlightedTitle}</div>
      <div class="result-text">${highlightedText}</div>
    `;
    item.setAttribute("data-href", href);

    item.addEventListener("click", () => navigateToHref(href));
    return item;
  }

  function highlightTerms(text, query) {
    if (!query.trim()) return text;
    const words = query.trim().split(/\s+/);
    const escapedWords = words.map((word) =>
      word.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&"),
    );
    const regex = new RegExp(`(${escapedWords.join("|")})`, "gi");
    return text.replace(regex, '<span class="highlight">$1</span>');
  }

  function getDynamicPath(targetFile) {
    // Get the content root from the HTML element
    const contentRoot =
      document.documentElement.getAttribute("data-content_root");
    return `${contentRoot}${targetFile}`;
  }

  function navigateToHref(href) {
    const finalUrl = getDynamicPath(href);
    window.location.href = finalUrl;
  }

  const searchBox = document
    .getElementById("search-bar")
    .querySelector(".bd-search input");

  searchBox.addEventListener("input", function () {
    const query = this.value.trim();
    if (query.length < parseInt(min_chars_for_search)) {
      document.getElementById("results").innerHTML = "";
      return;
    }
    performSearch(query);
  });

  searchBox.addEventListener("keydown", function (event) {
    const resultsContainer = document.getElementById("results");
    const resultItems = resultsContainer.querySelectorAll(".result-item");

    switch (event.key) {
      case "Enter":
        event.preventDefault(); // Prevent form submission
        if (currentIndex >= 0 && currentIndex < resultItems.length) {
          const href = resultItems[currentIndex].getAttribute("data-href");
          navigateToHref(href);
        } else if (resultItems.length > 0) {
          const href = resultItems[0].getAttribute("data-href");
          navigateToHref(href);
        }
        break;

      case "ArrowDown":
        if (resultItems.length > 0) {
          currentIndex = (currentIndex + 1) % resultItems.length; // Move down
          focusSelected(resultItems);
        }
        break;

      case "ArrowUp":
        if (resultItems.length > 0) {
          currentIndex =
            (currentIndex - 1 + resultItems.length) % resultItems.length; // Move up
          focusSelected(resultItems);
        }
        break;

      case "Tab":
        // Handle Tab key for navigation
        if (event.shiftKey) {
          // Shift + Tab: Move focus to the previous item
          if (currentIndex > 0) {
            currentIndex -= 1;
          } else {
            currentIndex = resultItems.length - 1; // Cycle to the last item
          }
        } else {
          // Tab: Move focus to the next item
          if (currentIndex < resultItems.length - 1) {
            currentIndex += 1;
          } else {
            currentIndex = 0; // Cycle to the first item
          }
        }
        event.preventDefault(); // Prevent default tab action
        focusSelected(resultItems, currentIndex);
        break;

      default:
        return; // Allow other keys to function normally
    }
  });

  function focusSelected(resultItems) {
    // Ensure currentIndex is valid
    if (currentIndex >= 0 && currentIndex < resultItems.length) {
      // Remove selected class from all items
      resultItems.forEach((item) => item.classList.remove("selected"));
      const currentItem = resultItems[currentIndex];
      currentItem.classList.add("selected"); // Add selected class

      // Apply native focus to the current item
      currentItem.focus();

      // Scroll the focused item into view
      currentItem.scrollIntoView({ block: "nearest" });
    }
  }
  fetch(searchPath)
    .then((response) =>
      response.ok
        ? response.json()
        : Promise.reject("Error: " + response.statusText),
    )
    .then((data) => initializeFuse(data))
    .catch((error) => console.error("Fetch operation failed:", error));
});
