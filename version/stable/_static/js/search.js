/**
 * @file search.js
 * @description Client-side search functionality using Fuse.js for the Ansys Sphinx Theme.
 */

const MAIN_PAGE_CONTENT = document.querySelector(".bd-main");
const FUSE_VERSION = "6.4.6";
let SEARCH_BAR,
  RESULTS_CONTAINER,
  SEARCH_INPUT,
  CURRENT_INDEX = -1,
  fuseInstance;

/**
 * Load fuse.js from CDN and initialize search functionality.
 */
require.config({
  paths: {
    fuse: `https://cdn.jsdelivr.net/npm/fuse.js@${FUSE_VERSION}/dist/fuse.min`,
  },
});

require(["fuse"], (Fuse) => {
  /**
   * Debounce utility to limit function execution rate.
   * @param {Function} func
   * @param {number} delay
   * @returns {Function}
   */
  const debounce = (func, delay) => {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), delay);
    };
  };

  /**
   * Truncate text for preview.
   * @param {string} text
   * @param {number} maxLength
   * @returns {string}
   */
  const truncateTextPreview = (text, maxLength = 200) =>
    text.length <= maxLength ? text : `${text.slice(0, maxLength)}...`;

  /**
   * Get full path using Sphinx's data-content_root.
   * @param {string} targetFile
   * @returns {string}
   */
  const getDynamicPath = (targetFile) => {
    const contentRoot =
      document.documentElement.getAttribute("data-content_root");
    return `${contentRoot}${targetFile}`;
  };

  /**
   * Navigate to a given URL.
   * @param {string} href
   */
  const navigateToHref = (href) => {
    window.location.href = getDynamicPath(href);
  };

  /**
   * Expand the search input UI.
   */
  function expandSearchInput() {
    RESULTS_CONTAINER.style.display = "flex";
    SEARCH_INPUT.classList.add("expanded");
    MAIN_PAGE_CONTENT.classList.add("blurred");
    SEARCH_INPUT.focus();

    // Fix overlapping on mobile view
    const modalSidebar = document.querySelector(
      "#pst-primary-sidebar-modal > div.sidebar-primary-items__start.sidebar-primary__section",
    );
    if (modalSidebar) modalSidebar.style.opacity = "0.1";
  }

  /**
   * Collapse and reset the search UI.
   */
  function collapseSearchInput() {
    RESULTS_CONTAINER.style.display = "none";
    SEARCH_INPUT.classList.remove("expanded");
    SEARCH_INPUT.value = "";
    MAIN_PAGE_CONTENT.classList.remove("blurred");
    CURRENT_INDEX = -1;

    const modalSidebar = document.querySelector(
      "#pst-primary-sidebar-modal > div.sidebar-primary-items__start.sidebar-primary__section",
    );
    if (modalSidebar) modalSidebar.style.opacity = "1";
  }

  /**
   * Show banner when no results found.
   */
  function noResultsFoundBanner() {
    RESULTS_CONTAINER.innerHTML = "";
    RESULTS_CONTAINER.style.display = "flex";
    const banner = document.createElement("div");
    banner.className = "warning-banner";
    banner.textContent =
      "No results found. Press Ctrl+Enter for extended search.";
    banner.style.fontStyle = "italic";
    RESULTS_CONTAINER.appendChild(banner);
  }

  /**
   * Show a temporary searching indicator.
   */
  function searchingForResultsBanner() {
    RESULTS_CONTAINER.innerHTML = "";
    RESULTS_CONTAINER.style.display = "flex";
    const banner = document.createElement("div");
    banner.className = "searching-banner";
    banner.textContent = "Searching...";
    banner.style.fontStyle = "italic";
    RESULTS_CONTAINER.appendChild(banner);
  }

  /**
   * Display search results from Fuse.
   * @param {Array} results
   */
  function displayResults(results) {
    RESULTS_CONTAINER.innerHTML = "";
    if (!results.length) return noResultsFoundBanner();

    const fragment = document.createDocumentFragment();
    results.forEach(({ item: { title, text, href } }) => {
      const resultItem = document.createElement("div");
      resultItem.className = "result-item";
      resultItem.dataset.href = href;
      resultItem.addEventListener("click", () => navigateToHref(href));

      const resultTitle = document.createElement("div");
      resultTitle.className = "result-title";
      resultTitle.textContent = title;

      const resultText = document.createElement("div");
      resultText.className = "result-text";
      resultText.textContent = truncateTextPreview(text);

      resultItem.append(resultTitle, resultText);
      fragment.appendChild(resultItem);
    });

    // Advanced Search Option
    const query = SEARCH_INPUT.value.trim();
    const advancedSearchItem = document.createElement("div");
    advancedSearchItem.className = "result-item advanced-search";
    advancedSearchItem.style.display = "flex";
    advancedSearchItem.style.justifyContent = "space-between";
    advancedSearchItem.style.alignItems = "center";
    advancedSearchItem.dataset.href = ADVANCE_SEARCH_PATH + "?q=" + query;
    advancedSearchItem.innerHTML = `<a href="${ADVANCE_SEARCH_PATH}?q=${query}">Show all results</a> <span style="font-size: 0.8em; color: gray;">Ctrl + Enter</span>`;
    advancedSearchItem.addEventListener("click", () => {
      window.location.href =
        ADVANCE_SEARCH_PATH + "?q=" + SEARCH_INPUT.value.trim();
    });

    fragment.appendChild(advancedSearchItem);
    RESULTS_CONTAINER.appendChild(fragment);
    RESULTS_CONTAINER.style.display = "flex";
  }

  /**
   * Focus the currently selected result item.
   * @param {NodeList} resultsItems
   */
  function focusSelected(resultsItems) {
    if (CURRENT_INDEX >= 0 && CURRENT_INDEX < resultsItems.length) {
      resultsItems.forEach((item) => item.classList.remove("selected"));
      const currentItem = resultsItems[CURRENT_INDEX];
      currentItem.classList.add("selected");
      currentItem.focus();
      currentItem.scrollIntoView({ block: "nearest" });
    }
  }

  /**
   * Handle keyboard navigation inside search input.
   * @param {KeyboardEvent} event
   */
  function handleKeyDownSearchInput(event) {
    const resultItems = RESULTS_CONTAINER.querySelectorAll(".result-item");
    switch (event.key) {
      case "Tab":
        event.preventDefault();
        break;
      case "Escape":
        collapseSearchInput();
        break;
      case "Enter":
        event.preventDefault();
        if (event.ctrlKey || event.metaKey) {
          const query = SEARCH_INPUT.value.trim();
          window.location.href = ADVANCE_SEARCH_PATH + "?q=" + query;
        } else if (CURRENT_INDEX >= 0 && CURRENT_INDEX < resultItems.length) {
          navigateToHref(resultItems[CURRENT_INDEX].dataset.href);
        } else if (resultItems.length > 0) {
          navigateToHref(resultItems[0].dataset.href);
        }
        break;
      case "ArrowDown":
        if (resultItems.length > 0) {
          CURRENT_INDEX = (CURRENT_INDEX + 1) % resultItems.length;
          focusSelected(resultItems);
        }
        break;
      case "ArrowUp":
        if (resultItems.length > 0) {
          CURRENT_INDEX =
            (CURRENT_INDEX - 1 + resultItems.length) % resultItems.length;
          focusSelected(resultItems);
        }
        break;
      default:
        if (
          event.ctrlKey ||
          event.altKey ||
          event.metaKey ||
          event.key === "Control" ||
          event.key === "Alt"
        ) {
          return;
        }
        if (
          document.documentElement.getAttribute("data-fuse_active") === "true"
        ) {
          searchingForResultsBanner();
        } else {
          RESULTS_CONTAINER.style.display = "none";
        }
        handleSearchInput();
    }
  }

  /**
   * Handle search query input with debounce.
   */
  const handleSearchInput = debounce(
    () => {
      const query = SEARCH_INPUT.value.trim();
      if (!query) return (RESULTS_CONTAINER.style.display = "none");

      const searchResults = fuseInstance.search(query, {
        limit: parseInt(SEARCH_OPTIONS.limit),
      });
      displayResults(searchResults);
    },
    parseInt(SEARCH_OPTIONS.delay) || 300,
  );

  /**
   * Initialize and bind search elements.
   */
  function setupSearchElements() {
    if (window.innerWidth < 1200) {
      SEARCH_BAR = document.querySelector(
        "div.sidebar-header-items__end #search-bar",
      );
      RESULTS_CONTAINER = document.querySelector(
        "div.sidebar-header-items__end .static-search-results",
      );
    } else {
      SEARCH_BAR = document.getElementById("search-bar");
      RESULTS_CONTAINER = document.querySelector(".static-search-results");
    }
    if (!SEARCH_BAR) {
      console.warn("SEARCH_BAR not found for current view.");
      return;
    }
    SEARCH_INPUT = SEARCH_BAR.querySelector(".bd-search input.form-control");
    if (SEARCH_INPUT) {
      SEARCH_INPUT.addEventListener("click", expandSearchInput);
      SEARCH_INPUT.addEventListener("keydown", handleKeyDownSearchInput);
    }
  }

  /**
   * Handle global keydown events for search shortcuts.
   * @param {KeyboardEvent} event
   */
  function handleGlobalKeyDown(event) {
    if (event.key === "Escape") collapseSearchInput();
    else if (event.key === "k" && event.ctrlKey) expandSearchInput();
  }

  /**
   * Collapse search if clicking outside.
   * @param {MouseEvent} event
   */
  function handleGlobalClick(event) {
    if (
      !RESULTS_CONTAINER.contains(event.target) &&
      event.target !== SEARCH_INPUT
    ) {
      collapseSearchInput();
    }
  }

  /**
   * Initialize Fuse with the given data and options.
   * @param {Array} data
   * @param {Object} options
   */
  function initializeFuse(data, options) {
    fuseInstance = new Fuse(data, options);
    document.documentElement.setAttribute("data-fuse_active", "true");
  }

  // Initialize search functionality on page load
  setupSearchElements();
  window.addEventListener("resize", debounce(setupSearchElements, 250));
  document.addEventListener("keydown", handleGlobalKeyDown);
  document.addEventListener("click", handleGlobalClick);

  fetch(SEARCH_FILE)
    .then((response) => {
      if (!response.ok)
        throw new Error(`[AST]: HTTPS error ${response.statusText}`);
      return response.json();
    })
    .then((SEARCH_DATA) => initializeFuse(SEARCH_DATA, SEARCH_OPTIONS))
    .catch((error) =>
      console.error(`[AST]: Cannot fetch ${SEARCH_FILE}`, error.message),
    );
});
