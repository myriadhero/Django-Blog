(function () {
  const allCarousels = document.querySelectorAll(".swiper");

  for (let carousel of allCarousels) {
    const carouselSelector = "#" + carousel.id;

    const swiper = new Swiper(carouselSelector, {
      // Optional parameters
      // Default parameters
      slidesPerView: 2,
      spaceBetween: 30,
      // Responsive breakpoints
      breakpoints: {
        // touch devices
        769: {
          slidesPerView: 3,
        },
        // desktop
        1024: {
          slidesPerView: 4,
        },
        // widescreen
        1216: {
          slidesPerView: 5,
        },
      },

      // If we need pagination
      pagination: {
        el: `${carouselSelector} .swiper-pagination`,
        clickable: true,
        dynamicBullets: true,
        dynamicMainBullets: 3,
      },

      // Navigation arrows
      navigation: {
        nextEl: `${carouselSelector} .swiper-button-next`,
        prevEl: `${carouselSelector} .swiper-button-prev`,
      },

      // And if we need scrollbar
      // scrollbar: {
      //   el: '.swiper-scrollbar',
      // },

      freemode: true,
    });
  }
})();

(function get_scrollbar_width() {
  // Get window width including scrollbar.
  const withScrollBar = window.innerWidth;

  // Get window width excluding scrollbar.
  const noScrollBar = document
    .querySelector("html")
    .getBoundingClientRect().width;

  // Calc the scrollbar width.
  const scrollbarWidth = parseInt(withScrollBar - noScrollBar, 10) + "px";

  // Update the CSS custom property value.
  let root = document.documentElement;
  root.style.setProperty("--scrollbar-width", scrollbarWidth);
})();
