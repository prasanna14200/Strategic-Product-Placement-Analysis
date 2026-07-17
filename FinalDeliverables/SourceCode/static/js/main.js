/**
 * Strategic Product Placement Analysis - Main JavaScript
 * Handles animations, Tableau embedding, counters, and UI interactions.
 */

(function () {
    'use strict';

    // -------------------------------------------------------------------------
    // Initialize on DOM ready
    // -------------------------------------------------------------------------
    document.addEventListener('DOMContentLoaded', function () {
        initAOS();
        initNavbarScroll();
        initCounters();
        initTableauEmbeds();
        initFilterChips();
        initSmoothScroll();
    });

    // -------------------------------------------------------------------------
    // AOS (Animate On Scroll) Initialization
    // -------------------------------------------------------------------------
    function initAOS() {
        if (typeof AOS !== 'undefined') {
            AOS.init({
                duration: 800,
                easing: 'ease-out-cubic',
                once: true,
                offset: 80,
                disable: window.matchMedia('(prefers-reduced-motion: reduce)').matches
            });
        }
    }

    // -------------------------------------------------------------------------
    // Navbar scroll effect
    // -------------------------------------------------------------------------
    function initNavbarScroll() {
        const navbar = document.getElementById('mainNavbar');
        if (!navbar) return;

        function updateNavbar() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }

        window.addEventListener('scroll', updateNavbar, { passive: true });
        updateNavbar();
    }

    // -------------------------------------------------------------------------
    // Animated number counters for KPI cards
    // -------------------------------------------------------------------------
    function initCounters() {
        const counters = document.querySelectorAll('.counter[data-target]');
        if (counters.length === 0) return;

        const observerOptions = {
            threshold: 0.5,
            rootMargin: '0px'
        };

        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        counters.forEach(function (counter) {
            observer.observe(counter);
        });
    }

    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-target'), 10);
        if (isNaN(target)) return;

        const duration = 1500;
        const startTime = performance.now();
        const startValue = 0;

        function formatNumber(num) {
            return num.toLocaleString('en-US');
        }

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(startValue + (target - startValue) * eased);

            element.textContent = formatNumber(current);

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                element.textContent = formatNumber(target);
            }
        }

        requestAnimationFrame(update);
    }

    // -------------------------------------------------------------------------
    // Tableau Public embed initialization
    // -------------------------------------------------------------------------
    function initTableauEmbeds() {
        const dashboardEmbed = document.getElementById('tableauDashboardEmbed');
        const storyEmbed = document.getElementById('tableauStoryEmbed');

        if (dashboardEmbed) {
            const dashboardUrl = dashboardEmbed.getAttribute('data-tableau-url');
            if (dashboardUrl && isValidTableauUrl(dashboardUrl)) {
                embedTableauViz(dashboardEmbed, dashboardUrl, 'dashboardPlaceholder');
            }
        }

        if (storyEmbed) {
            const storyUrl = storyEmbed.getAttribute('data-tableau-url');
            if (storyUrl && isValidTableauUrl(storyUrl)) {
                embedTableauViz(storyEmbed, storyUrl, 'storyPlaceholder');
            }
        }
    }

    function isValidTableauUrl(url) {
        if (!url) return false;
        // Accept Tableau Public and Tableau Cloud/Online domains
        return url.includes('tableau.com') &&
               !url.includes('ProductPositioningAnalysis/Dashboard') &&
               !url.includes('ProductPositioningAnalysis/Story');
    }

    function embedTableauViz(container, url, placeholderId) {
        const placeholder = document.getElementById(placeholderId);
        if (placeholder) {
            placeholder.style.display = 'none';
        }

        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'tableau-loading';
        loadingDiv.innerHTML = '<div class="spinner"></div><p>Loading Tableau visualization...</p>';
        container.appendChild(loadingDiv);

        loadTableauApi(function () {
            container.removeChild(loadingDiv);

            const vizDiv = document.createElement('div');
            vizDiv.className = 'tableauViz';
            vizDiv.id = container.id + 'Viz';
            container.appendChild(vizDiv);

            const options = {
                hideTabs: false,
                hideToolbar: false,
                width: '100%',
                // Let CSS control sizing for responsiveness; use 100% here
                height: '100%',
                device: 'desktop'
            };

            try {
                const viz = new tableau.Viz(vizDiv, url, options);
                viz.addEventListener(tableau.TableauEventName.FIRST_INTERACTIVE, function () {
                    console.log('Tableau viz loaded:', url);
                });
            } catch (err) {
                console.error('Tableau embed error:', err);
                showEmbedError(container, placeholderId);
            }
        });
    }

    function loadTableauApi(callback) {
        if (typeof tableau !== 'undefined' && tableau.Viz) {
            callback();
            return;
        }

        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://public.tableau.com/javascripts/api/tableau-2.min.js';
        script.onload = callback;
        script.onerror = function () {
            console.error('Failed to load Tableau JavaScript API');
        };
        document.head.appendChild(script);
    }

    function showEmbedError(container, placeholderId) {
        const placeholder = document.getElementById(placeholderId);
        if (placeholder) {
            placeholder.style.display = 'flex';
        }
    }

    // -------------------------------------------------------------------------
    // Filter chip interaction (visual only on Flask pages)
    // -------------------------------------------------------------------------
    function initFilterChips() {
        const chips = document.querySelectorAll('.filter-chip');
        chips.forEach(function (chip) {
            chip.addEventListener('click', function () {
                chips.forEach(function (c) { c.classList.remove('active'); });
                chip.classList.add('active');
            });
        });
    }

    // -------------------------------------------------------------------------
    // Smooth scroll for anchor links
    // -------------------------------------------------------------------------
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
            anchor.addEventListener('click', function (e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;

                const target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    const offset = 80;
                    const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
                    window.scrollTo({ top: top, behavior: 'smooth' });
                }
            });
        });
    }

    // -------------------------------------------------------------------------
    // API helper - fetch KPIs dynamically (optional enhancement)
    // -------------------------------------------------------------------------
    window.fetchKPIs = function () {
        return fetch('/api/kpis')
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (data.status === 'success') {
                    return data.data;
                }
                throw new Error(data.message || 'Failed to fetch KPIs');
            });
    };

})();
