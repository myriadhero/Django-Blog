(function () {
    const swiper = new Swiper('.swiper', {
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
            }
        },

        // If we need pagination
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },

        // Navigation arrows
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },

        // And if we need scrollbar
        // scrollbar: {
        //   el: '.swiper-scrollbar',
        // }, 
    });
})();

(function get_scrollbar_width() {

    // Get window width including scrollbar.
    const withScrollBar = window.innerWidth;

    // Get window width excluding scrollbar.
    const noScrollBar = document.querySelector("html").getBoundingClientRect().width;

    // Calc the scrollbar width.
    const scrollbarWidth = parseInt((withScrollBar - noScrollBar), 10) + 'px';

    // Update the CSS custom property value.
    let root = document.documentElement;
    root.style.setProperty('--scrollbar-width', scrollbarWidth);

})();