/**
 * search-main.js
 *
 * Main search logic for the documentation site. Handles search index loading, filtering, and UI updates.
 * Uses Fuse.js for fuzzy searching and IndexedDB for caching search data.
 *
 */

// DOM Elements
const SEARCH_BAR = document.getElementById("search-bar");
const SEARCH_INPUT = SEARCH_BAR.querySelector(".bd-search input.form-control");

// Configure RequireJS for Fuse.js
require.config({
  paths: {
    fuse: "https://cdn.jsdelivr.net/npm/fuse.js@6.6.2/dist/fuse.min",
  },
});

/**
 * Open or create an IndexedDB database for caching search indexes.
 * @param {string} name - Name of the database.
 * @param {number} version - Version of the database.
 * @returns {Promise<IDBDatabase>} Promise resolving to the database instance.
 */
function openDB(name = "search-cache", version = 1) {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(name, version);
    request.onerror = () => {
      console.error("IndexedDB open error:", request.error);
      reject(request.error);
    };
    request.onsuccess = () => {
      resolve(request.result);
    };
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains("indexes")) {
        db.createObjectStore("indexes");
      }
    };
  });
}

/**
 * Retrieve a value from IndexedDB by key.
 * @param {string} key - The key to look up in the object store.
 * @returns {Promise<any>} Promise resolving to the retrieved value.
 */
async function getFromIDB(key) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction("indexes", "readonly");
    const store = transaction.objectStore("indexes");
    const request = store.get(key);
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

/**
 * Save a key-value pair to IndexedDB.
 * @param {string} key - The key to store the value under.
 * @param {any} value - The value to store.
 * @returns {Promise<boolean>} Promise resolving when saving is complete.
 */
async function saveToIDB(key, value) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction("indexes", "readwrite");
    const store = transaction.objectStore("indexes");
    const request = store.put(value, key);
    request.onsuccess = () => resolve(true);
    request.onerror = () => {
      console.error("Failed to save to IndexedDB:", request.error);
      reject(request.error);
    };
  });
}

/**
 * Main search logic, loaded after Fuse.js is available.
 */
require(["fuse"], function (Fuse) {
  let fuse;
  let searchData = [];
  let selectedObjectIDs = [];
  let selectedLibraries = [];
  const libSearchData = {};
  let selectedFilter = new Set();

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
   * Initialize the search system by loading the document search index and library indexes.
   * Sets up filter dropdowns and triggers initial search if needed.
   */
  async function initializeSearch() {
    try {
      const cacheKey = "main-search-index";
      let data = await getFromIDB(cacheKey);
      if (!data) {
        const response = await fetch(SEARCH_FILE);
        data = await response.json();
        await saveToIDB(cacheKey, data);
      }
      searchData = data;
      fuse = new Fuse(searchData, SEARCH_OPTIONS);

      // Load library search data
      const allLibs = Object.keys(EXTRA_SOURCES);
      for (const lib of allLibs) {
        const cacheKey = `lib-search-${lib}`;
        let libData = await getFromIDB(cacheKey);
        if (!libData) {
          const libPath = EXTRA_SOURCES[lib];
          const url = `${libPath}/_static/search.json`;
          const res = await fetch(url);
          libData = await res.json();
          await saveToIDB(cacheKey, libData);
        }
        libSearchData[lib] = libData;
      }
      setupFilterDropdown();
      showObjectIdDropdown();
      showLibraryDropdown();
    } catch (err) {
      console.error("Search init failed", err);
    }
  }

  /**
   * Sets up the filter dropdown and its toggle interactions in the sidebar.
   */
  function setupFilterDropdown() {
    const dropdownContainer = document.getElementById("search-sidebar");
    const filters = [
      {
        name: "Documents",
        dropdownId: "objectid-dropdown",
        callback: showObjectIdDropdown,
      },
      {
        name: "Library",
        dropdownId: "library-dropdown",
        callback: showLibraryDropdown,
      },
    ];
    // Remove the library filter if no libraries
    if (Object.keys(EXTRA_SOURCES).length === 0) {
      filters.splice(1, 1);
    }
    filters.forEach(({ name, dropdownId, callback }) => {
      const toggleDiv = document.createElement("div");
      toggleDiv.className = "search-page-sidebar toggle-section";
      toggleDiv.dataset.target = dropdownId;
      const icon = document.createElement("span");
      icon.className = "toggle-icon";
      icon.textContent = "▼";
      icon.style.fontSize = "12px";
      const label = document.createElement("span");
      label.className = "toggle-label";
      label.textContent = name;
      toggleDiv.append(icon, label);
      const dropdown = document.createElement("div");
      dropdown.id = dropdownId;
      dropdown.className = "dropdown-menu show";
      dropdown.style.display = "block";
      dropdown.style.marginTop = "10px";
      // Add event listener to toggle the dropdown
      toggleDiv.addEventListener("click", () => {
        const isVisible = dropdown.style.display === "block";
        dropdown.style.display = isVisible ? "none" : "block";
        icon.textContent = isVisible ? "▶" : "▼";
        if (isVisible) {
          selectedFilter.delete(name);
          toggleDiv.classList.remove("active");
        } else {
          selectedFilter.add(name);
          toggleDiv.classList.add("active");
          callback?.();
        }
        performSearch();
      });
      dropdownContainer.append(toggleDiv, dropdown);
    });
  }

  /**
   * Show the object ID dropdown for document filtering.
   */
  function showObjectIdDropdown() {
    const dropdown = document.getElementById("objectid-dropdown");
    dropdown.innerHTML = "";
    const objectIDs = [
      ...new Set(searchData.map((item) => item.objectID)),
    ].filter(Boolean);
    objectIDs.forEach((id) => {
      const checkbox = createCheckboxItem(id, selectedObjectIDs, () => {
        renderSelectedChips();
        performSearch();
      });
      dropdown.appendChild(checkbox);
    });
    dropdown.style.display = "block";
    renderSelectedChips();
  }

  /**
   * Show the library dropdown for library filtering.
   */
  function showLibraryDropdown() {
    const dropdown = document.getElementById("library-dropdown");
    dropdown.innerHTML = "";
    for (const lib in EXTRA_SOURCES) {
      const checkbox = createCheckboxItem(lib, selectedLibraries, () => {
        renderSelectedChips();
        performSearch();
      });
      dropdown.appendChild(checkbox);
    }
    dropdown.style.display = "block";
    renderSelectedChips();
  }

  /**
   * Create a checkbox item for a filter dropdown.
   * @param {string} value - Value for the checkbox.
   * @param {Array} selectedArray - Array of selected values.
   * @param {Function} onChange - Callback on change.
   * @returns {HTMLDivElement} Checkbox item div.
   */
  function createCheckboxItem(value, selectedArray, onChange) {
    const div = document.createElement("div");
    div.className = "checkbox-item";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = value;
    checkbox.style.margin = "8px";
    checkbox.checked = selectedArray.includes(value);
    checkbox.onchange = (e) => {
      if (e.target.checked) {
        selectedArray.push(value);
      } else {
        const index = selectedArray.indexOf(value);
        if (index > -1) selectedArray.splice(index, 1);
      }
      onChange();
    };
    const label = document.createElement("label");
    label.textContent = value;
    div.appendChild(checkbox);
    div.appendChild(label);
    return div;
  }

  /**
   * Render chips for selected filters and bind remove logic.
   */
  function renderSelectedChips() {
    const container = document.getElementById("selected-chips");
    container.innerHTML = "";
    const renderChip = (value, type, selectedArray) => {
      const chip = document.createElement("div");
      chip.className = "chip";
      chip.textContent = `${value} (${type})`;
      const removeBtn = document.createElement("button");
      removeBtn.className = "remove-btn";
      removeBtn.innerHTML = "&times;";
      removeBtn.onclick = () => {
        const index = selectedArray.indexOf(value);
        if (index !== -1) selectedArray.splice(index, 1);
        renderSelectedChips();
        if (type === "Documents") showObjectIdDropdown();
        if (type === "Library") showLibraryDropdown();
        performSearch();
      };
      chip.appendChild(removeBtn);
      container.appendChild(chip);
    };
    selectedObjectIDs.forEach((id) =>
      renderChip(id, "Documents", selectedObjectIDs),
    );
    selectedLibraries.forEach((lib) =>
      renderChip(lib, "Library", selectedLibraries),
    );
  }

  /**
   * Perform the search and update the results UI.
   */
  async function performSearch() {
    const query = document.getElementById("search-input").value.trim();
    if (!fuse) return;
    const resultsContainer = document.getElementById("search-results");
    resultsContainer.innerHTML = "Searching...";
    let docResults = [];
    let libResults = [];
    const resultLimit = getSelectedResultLimit();
    // Search in internal documents
    if (selectedFilter.size === 0 || selectedFilter.has("Documents")) {
      docResults = fuse
        .search(query, { limit: resultLimit })
        .map((r) => r.item);
      if (selectedObjectIDs.length > 0) {
        docResults = docResults.filter((item) =>
          selectedObjectIDs.includes(item.objectID),
        );
      }
    }
    // Search in selected libraries
    for (const lib of selectedLibraries) {
      const libBaseUrl = EXTRA_SOURCES[lib];
      const cacheKey = `lib-search-${lib}`;
      try {
        const data = await getFromIDB(cacheKey);
        if (data) {
          const enrichedEntries = data.map((entry) => ({
            title: entry.title,
            text: entry.text,
            section: entry.section,
            link: `${libBaseUrl}${entry.href}`,
            source: lib,
          }));
          const libFuse = new Fuse(enrichedEntries, SEARCH_OPTIONS);
          const results = libFuse
            .search(query, { limit: resultLimit })
            .map((r) => r.item);
          libResults.push(...results);
        }
      } catch (err) {
        console.error(`Error accessing cache for ${lib}:`, err);
      }
    }
    // Merge and show results
    const mergedResults = [...docResults, ...libResults];
    if (mergedResults.length === 0) {
      resultsContainer.innerHTML = "<p>No results found.</p>";
      return;
    }
    const highlightedResults = highlightResults(mergedResults, query);
    displayResults(highlightedResults);
  }

  /**
   * Highlight search query in the results.
   * @param {Array} results - Array of result objects.
   * @param {string} query - Search query.
   * @returns {Array} Highlighted results.
   */
  function highlightResults(results, query) {
    const regex = new RegExp(`(${query})`, "gi");
    return results
      .map((result) => {
        const matchIndex = result.text
          .toLowerCase()
          .indexOf(query.toLowerCase());
        if (matchIndex === -1) return null;
        const contextLength = 100;
        const start = Math.max(0, matchIndex - contextLength);
        const end = Math.min(result.text.length, matchIndex + contextLength);
        let snippet = result.text.slice(start, end);
        if (start > 0) snippet = "…" + snippet;
        if (end < result.text.length) snippet += "…";
        return {
          ...result,
          title: result.title.replace(
            regex,
            `<span class="search-highlight">$1</span>`,
          ),
          text: snippet.replace(
            regex,
            `<span class="search-highlight">$1</span>`,
          ),
        };
      })
      .filter(Boolean);
  }

  /**
   * Display the final search results on the UI.
   * @param {Array} results - Array of result objects.
   */
  function displayResults(results) {
    const container = document.getElementById("search-results");
    container.innerHTML = "";
    results.forEach((item) => {
      const div = document.createElement("div");
      div.className = "result-item";
      const title = document.createElement("a");
      title.href = item.href || item.link || "#";
      title.target = "_blank";
      title.innerHTML = item.title || "Untitled";
      title.className = "result-title";
      div.appendChild(title);
      if (item.text) {
        const text = document.createElement("p");
        text.innerHTML = item.text;
        text.className = "result-text";
        div.appendChild(text);
      }
      if (item.source) {
        const source = document.createElement("p");
        source.className = "checkmark";
        source.textContent = `Source: ${item.source}`;
        div.appendChild(source);
      }
      container.appendChild(div);
    });
  }

  /**
   * Get the selected result limit from the dropdown.
   * @returns {number} Result limit.
   */
  function getSelectedResultLimit() {
    const select = document.getElementById("result-limit");
    return parseInt(select.value, 10) || 10;
  }

  // --- Event Handlers and Initialization ---

  /**
   * Debounced handler for search input changes.
   */
  const handleSearchInput = debounce(
    () => {
      const query = document.getElementById("search-input").value.trim();
      if (query.length > 0) {
        performSearch();
      }
    },
    parseInt(SEARCH_OPTIONS.delay) || 300,
  );

  /**
   * Utility to get element by ID.
   * @param {string} id - Element ID.
   * @returns {HTMLElement} DOM element.
   */
  const $ = (id) => document.getElementById(id);

  // Elements
  const searchInput = $("search-input");
  const resultLimit = $("result-limit");

  // Initialize search input if query param is present
  const urlParams = new URLSearchParams(window.location.search);
  const initialQuery = urlParams.get("q");
  if (initialQuery) {
    searchInput.value = initialQuery;
  }

  /**
   * Unified search trigger for input events.
   */
  const triggerSearch = () => {
    const query = searchInput.value.trim();
    if (query) {
      handleSearchInput();
    }
  };

  // Set up event listeners
  searchInput.addEventListener("input", triggerSearch);
  resultLimit?.addEventListener("change", performSearch);
  SEARCH_BAR.addEventListener("input", (e) => {
    searchInput.value = e.target.value;
    triggerSearch();
  });

  // Initialize search engine/data
  initializeSearch();

  // Optional: trigger on page load if query param was present
  if (initialQuery) {
    triggerSearch();
  }
});
