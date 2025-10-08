/**
 * Navbar Scroll Effect
 * Makes the navbar transparent initially and adds background on scroll
 */

(function () {
    'use strict';

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initNavbarScroll);
    } else {
        initNavbarScroll();
    }

    function initNavbarScroll() {
        const navbar = document.getElementById('navbar');
        if (!navbar) return;

        const SCROLL_THRESHOLD = 50;
        const NAVBAR_CLASSES = ['backdrop-blur-md', 'bg-white/80', 'shadow-sm'];

        function updateNavbar() {
            const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

            if (currentScroll > SCROLL_THRESHOLD) {
                navbar.classList.add(...NAVBAR_CLASSES);
            } else {
                navbar.classList.remove(...NAVBAR_CLASSES);
            }
        }

        // Initial check
        updateNavbar();

        // Listen to scroll events with throttling for better performance
        let ticking = false;
        window.addEventListener('scroll', function () {
            if (!ticking) {
                window.requestAnimationFrame(function () {
                    updateNavbar();
                    ticking = false;
                });
                ticking = true;
            }
        }, { passive: true });
    }
})();

