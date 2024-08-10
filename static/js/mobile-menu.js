const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar-menu');
const navLogo = document.querySelector('.navbar-logo');
const body = document.querySelector('body');
const html = document.querySelector('html');


//Mobile Menu Display

const mobileMenu = () => {
  menu.classList.toggle('is-active');
  menuLinks.classList.toggle('active');
  body.classList.toggle('active');
  html.classList.toggle('active');
};

menu.addEventListener('click', mobileMenu);



