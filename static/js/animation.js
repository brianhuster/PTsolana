
const observer = new IntersectionObserver ((entries) => {

  entries.forEach((entry) => {

    console.log(entry)
    if (entry.isIntersecting) {
      entry.target.classList.add('show');
      
    }

    else {
      entry.target.classList.remove('show');
    }

  });

});


const hiddenElementsLeft = document.querySelectorAll('.hiddenLeft');

const hiddenElementsRight = document.querySelectorAll('.hiddenRight');


hiddenElementsLeft.forEach((el) => observer.observe(el));

hiddenElementsRight.forEach((el) => observer.observe(el));





gsap.registerPlugin(ScrollTrigger);


//Header Animations

gsap.from('.logo-animate', 1, {
  opacity: 0,
  x: -20,
  ease: Expo.easeInOut 
},0.08);

gsap.from('.navbar-animate', 1, {
  duration: 0.6,
  opacity: 0,
  x: 25,
  stagger: 0.15,
  ease: Power3.easeInOut
}, 0.06);




//Index Page Animations

//Hero Animations

gsap.from('.hero-animate-p',  {
  duration: 0.6,
  opacity: 0,
  y: -25,
  stagger: 0.15 
});


gsap.from('.hero-title-animate', 1, {
  duration: 0.25,
  opacity: 0,
  y: 30,
  x: 10,
  ease: Power3.easeInOut
}, 0.08);

gsap.from('.hero-title-animate-2', 1, {
  duration: 0.25,
  opacity: 0,
  delay: 0.2,
  y: 30,
  x: 10,
  ease: Power3.easeInOut
}, 0.08);

gsap.from('.delay-span-animate', 1, {
  duration: 0.3,
  opacity: 0,
  delay: 0.4,
  y: 25,
  x: 10,
  ease: Expo.easeInOut
}, 0.06);


//Services Animation

gsap.from('.img-animate-top-right', 1, {
  scrollTrigger: '.img-animate-top-right',
  duration: 0.8,
  blur: 50,
  opacity: 0,
  x: 10,
  y: -20
}, 0.06);

gsap.from('.img-animate-bottom-right', 1, {
  scrollTrigger: '.img-animate-bottom-right',
  duration: 0.8,
  blur: 50,
  opacity: 0,
  x: 10,
  y: 20
}, 0.06);

gsap.from('.img-animate-bottom-left', 1, {
  scrollTrigger: '.img-animate-bottom-left',
  duration: 0.8,
  blur: 50,
  opacity: 0,
  x: -10,
  y: 20
}, 0.06);



//Personal Trainers Animation

gsap.from('.animate-team', {
  scrollTrigger: '.animate-team',
  duration: 1,
  opacity: 0,
  y: -100,
  stagger: 0.3,
  delay: 0.2
});

gsap.from('.animate-email', {
  scrollTrigger: '.animate-email',
  duration: 0.4,
  opacity: 0,
  y: -120,
  stagger: 0.2,
  delay: 0.4
});



// Memberships Animations

gsap.from('.memb-animate-left', 1, {
  scrollTrigger: '.memb-animate-left',
  duration: 1,
  opacity: 0,
  x: -500,
  stagger: 0.15,
  blur: 20
}, 0.06);


gsap.from('.memb-animate-right', 1, {
  scrollTrigger: '.memb-animate-right',
  duration: 1,
  opacity: 0,
  x: 500,
  stagger: 0.15,
  blur: 20
}, 0.06);


gsap.from('.memb-animate-bottom', 1, {
  scrollTrigger: '.memb-animate-bottom',
  duration: 1,
  opacity: 0,
  y: 500,
  stagger: 0.15,
  blur: 20,
  delay: 0.05
}, 0.06);

















