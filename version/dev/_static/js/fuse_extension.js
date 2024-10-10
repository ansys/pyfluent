const searchBar = document.getElementById("search-bar");
const searchBarBox = searchBar.querySelector(".bd-search input");
resultsContainer = document.getElementById("results");
const content = document.querySelector(".bd-main");

// Function to expand the search bar and display results
function expandSearchBox() {
  searchBarBox.classList.add("expanded");
  content.classList.add("blurred");
  searchBarBox.focus();

  if (searchBarBox.value.trim().length >= parseInt(min_chars_for_search)) {
    resultsContainer.style.display = "flex";
  }
}

// Expand search box on click
searchBarBox.addEventListener("click", expandSearchBox);

// Keydown event handler using switch
document.addEventListener("keydown", function (event) {
  switch (event.key) {
    case "k":
      if (event.ctrlKey) {
        expandSearchBox();
      }
      break;
    case "Escape":
      resultsContainer.style.display = "none";
      searchBarBox.classList.remove("expanded");
      content.classList.remove("blurred");
      break;
  }
});

// Hide the results and collapse the search box on outside click
document.addEventListener("click", function (event) {
  if (
    !resultsContainer.contains(event.target) &&
    event.target !== searchBarBox
  ) {
    resultsContainer.style.display = "none";
    searchBarBox.classList.remove("expanded");
    content.classList.remove("blurred");
  }
});
