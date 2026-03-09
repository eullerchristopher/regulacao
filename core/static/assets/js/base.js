/*=============== MENU ===============*/

document.addEventListener('DOMContentLoaded', () => {
    const navMenu = document.getElementById("nav-menu");
    const navToggle = document.getElementById("nav-toggle");
    const navClose = document.getElementById("nav-close");
    const navLinks = document.querySelectorAll(".nav_link");

    /* Abrir menu */
    if (navToggle) {
        navToggle.addEventListener("click", () => {
            navMenu.classList.add("show-menu");
        });
    }

    /* Fechar menu */
    if (navClose) {
        navClose.addEventListener("click", () => {
            navMenu.classList.remove("show-menu");
        });
    }

    /* Fechar ao clicar em um link */
    navLinks.forEach(link => {
        link.addEventListener("click", () => {
            navMenu.classList.remove("show-menu");
        });
    });
});