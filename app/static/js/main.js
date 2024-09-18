// Toggle mobile menu visibility
document.querySelector(".hamburger").addEventListener("click", function () {
  const nav = document.querySelector("#mobile-nav");
  if (nav.style.display === "flex") {
    nav.style.display = "none";
  } else {
    nav.style.display = "flex";
  }
});
