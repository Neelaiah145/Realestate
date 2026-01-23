document.addEventListener("DOMContentLoaded", function () {
    const toggles = document.querySelectorAll(".toggle-link");

    toggles.forEach(function (toggle) {
        toggle.addEventListener("click", function (e) {
            e.preventDefault();
            const parentLi = this.closest(".has-submenu");
            parentLi.classList.toggle("open");
        });
    });
});