const headerToggleBtn = document.querySelector(".header-toggleBtn");
const categories = document.querySelector(".categories");
const header = document.querySelector("header");

const handleClickToggleBtn = () => {
  categories.classList.toggle("active");
};

const handleScroll = () => {
  if (window.scrollY > 50) {
    header.style.backgroundColor = "rgb(20, 20, 20)";
  } else header.style.backgroundColor = "transparent";
};

function init() {
  headerToggleBtn.addEventListener("click", handleClickToggleBtn);
  window.addEventListener("scroll", handleScroll);
}

init();
