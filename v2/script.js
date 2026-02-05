// ===================================
// Sparkling Solutions - Main JavaScript
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initHeroStats();
    initBeforeAfterSliders();
    initTestimonialCarousel();
    initPricingCalculator();
    initFAQ();
    initGallery();
    initContactForm();
    initSmoothScroll();
    initAnimations();
});

// ===================================
// Navigation
// ===================================
function initNavbar() {
    const navbar = document.getElementById('navbar');
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.querySelector('.nav-links');

    // Scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile menu toggle
    mobileToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        this.querySelector('i').classList.toggle('fa-bars');
        this.querySelector('i').classList.toggle('fa-times');
    });

    // Close mobile menu on link click
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', function() {
            navLinks.classList.remove('active');
            mobileToggle.querySelector('i').classList.add('fa-bars');
            mobileToggle.querySelector('i').classList.remove('fa-times');
        });
    });
}

// ===================================
// Hero Statistics Counter
// ===================================
function initHeroStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    let animated = false;

    function animateStats() {
        statNumbers.forEach(stat => {
            const target = parseInt(stat.getAttribute('data-count'));
            const duration = 2000;
            const step = target / (duration / 16);
            let current = 0;

            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    stat.textContent = target.toLocaleString() + (stat.getAttribute('data-count') === '98' ? '%' : '+');
                    clearInterval(timer);
                } else {
                    stat.textContent = Math.floor(current).toLocaleString();
                }
            }, 16);
        });
    }

    // Intersection Observer for stats
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !animated) {
                animated = true;
                animateStats();
            }
        });
    }, { threshold: 0.5 });

    const heroStats = document.querySelector('.hero-stats');
    if (heroStats) {
        statsObserver.observe(heroStats);
    }
}

// ===================================
// Before/After Sliders
// ===================================
function initBeforeAfterSliders() {
    const sliders = document.querySelectorAll('.before-after-slider');

    sliders.forEach(slider => {
        const beforeImage = slider.querySelector('.before-image');
        const handle = slider.querySelector('.slider-handle');
        let isDragging = false;

        function updateSlider(x) {
            const rect = slider.getBoundingClientRect();
            let percentage = ((x - rect.left) / rect.width) * 100;
            percentage = Math.max(0, Math.min(100, percentage));
            beforeImage.style.width = percentage + '%';
            handle.style.left = percentage + '%';
        }

        handle.addEventListener('mousedown', (e) => {
            isDragging = true;
            e.preventDefault();
        });

        document.addEventListener('mousemove', (e) => {
            if (isDragging) {
                updateSlider(e.clientX);
            }
        });

        document.addEventListener('mouseup', () => {
            isDragging = false;
        });

        // Touch support
        handle.addEventListener('touchstart', (e) => {
            isDragging = true;
        });

        document.addEventListener('touchmove', (e) => {
            if (isDragging) {
                updateSlider(e.touches[0].clientX);
            }
        });

        document.addEventListener('touchend', () => {
            isDragging = false;
        });

        // Click to move
        slider.addEventListener('click', (e) => {
            if (e.target !== handle) {
                updateSlider(e.clientX);
            }
        });
    });
}

// ===================================
// Testimonial Carousel
// ===================================
function initTestimonialCarousel() {
    const track = document.getElementById('testimonialTrack');
    const prevBtn = document.getElementById('prevTestimonial');
    const nextBtn = document.getElementById('nextTestimonial');
    const dotsContainer = document.getElementById('carouselDots');

    if (!track || !prevBtn || !nextBtn) return;

    const cards = track.querySelectorAll('.testimonial-card');
    let currentIndex = 0;
    let cardsPerView = getCardsPerView();

    function getCardsPerView() {
        if (window.innerWidth < 768) return 1;
        if (window.innerWidth < 1024) return 2;
        return 3;
    }

    function createDots() {
        dotsContainer.innerHTML = '';
        const totalDots = Math.ceil(cards.length / cardsPerView);
        for (let i = 0; i < totalDots; i++) {
            const dot = document.createElement('button');
            dot.classList.add('carousel-dot');
            if (i === currentIndex) dot.classList.add('active');
            dot.addEventListener('click', () => goToSlide(i));
            dotsContainer.appendChild(dot);
        }
    }

    function updateCarousel() {
        const cardWidth = cards[0].offsetWidth + 24; // Include gap
        track.style.transform = `translateX(-${currentIndex * cardWidth}rem)`;
        
        // Update dots
        document.querySelectorAll('.carousel-dot').forEach((dot, index) => {
            dot.classList.toggle('active', index === currentIndex);
        });
    }

    function goToSlide(index) {
        const totalSlides = Math.ceil(cards.length / cardsPerView);
        currentIndex = index;
        if (currentIndex >= totalSlides) currentIndex = 0;
        if (currentIndex < 0) currentIndex = totalSlides - 1;
        updateCarousel();
    }

    function nextSlide() {
        goToSlide(currentIndex + 1);
    }

    function prevSlide() {
        goToSlide(currentIndex - 1);
    }

    prevBtn.addEventListener('click', prevSlide);
    nextBtn.addEventListener('click', nextSlide);

    // Auto-play
    let autoplay = setInterval(nextSlide, 5000);

    track.addEventListener('mouseenter', () => clearInterval(autoplay));
    track.addEventListener('mouseleave', () => {
        autoplay = setInterval(nextSlide, 5000);
    });

    // Handle resize
    window.addEventListener('resize', () => {
        const newCardsPerView = getCardsPerView();
        if (newCardsPerView !== cardsPerView) {
            cardsPerView = newCardsPerView;
            currentIndex = 0;
            createDots();
            updateCarousel();
        }
    });

    createDots();
    updateCarousel();
}

// ===================================
// Pricing Calculator
// ===================================
function initPricingCalculator() {
    const inputs = {
        propertyType: document.getElementById('propertyType'),
        bathrooms: document.getElementById('bathrooms'),
        serviceType: document.getElementById('serviceType'),
        frequency: document.getElementById('frequency'),
        steamSanitize: document.getElementById('steamSanitize'),
        laundry: document.getElementById('laundry'),
        windows: document.getElementById('windows'),
        fridge: document.getElementById('fridge'),
        pets: document.getElementById('pets'),
        cabinets: document.getElementById('cabinets')
    };

    const display = {
        total: document.getElementById('totalPrice'),
        base: document.getElementById('basePrice'),
        service: document.getElementById('serviceAdjust'),
        frequency: document.getElementById('frequencyDiscount'),
        addOns: document.getElementById('addOnsTotal')
    };

    const basePrices = {
        studio: 69,
        '1bed': 79,
        '2bed': 89,
        '3bed': 119,
        '4bed': 149,
        '5bed': 179
    };

    const bathroomPrices = {
        '1': 0,
        '1.5': 15,
        '2': 30,
        '2.5': 45,
        '3': 60,
        '4': 90
    };

    const serviceAdjustments = {
        'standard': 0,
        'deep': 80,
        'move': 180
    };

    const frequencyDiscounts = {
        'one-time': 0,
        'weekly': 0.10,
        'biweekly': 0.05,
        'monthly': 0.03
    };

    const addOnPrices = {
        steamSanitize: 35,
        laundry: 25,
        windows: 30,
        fridge: 25,
        pets: 15,
        cabinets: 20
    };

    function calculate() {
        let total = basePrices[inputs.propertyType.value];
        total += bathroomPrices[inputs.bathrooms.value];

        const serviceAdj = serviceAdjustments[inputs.serviceType.value];
        const freqDiscount = frequencyDiscounts[inputs.frequency.value];

        // Calculate add-ons
        let addOnsTotal = 0;
        Object.keys(addOnPrices).forEach(key => {
            if (inputs[key] && inputs[key].checked) {
                addOnsTotal += addOnPrices[key];
            }
        });

        // Apply service adjustment
        total += serviceAdj;

        // Apply frequency discount to base + add-ons
        const discountable = total;
        const discount = discountable * freqDiscount;

        // Add add-ons
        total += addOnsTotal;

        // Apply discount
        total = total - discount;

        // Update display
        display.total.textContent = '$' + Math.round(total);
        display.base.textContent = '$' + (basePrices[inputs.propertyType.value] + bathroomPrices[inputs.bathrooms.value]);
        display.service.textContent = (serviceAdj >= 0 ? '+' : '') + '$' + serviceAdj;
        display.frequency.textContent = '-' + '$' + Math.round(discount);
        display.addOns.textContent = '$' + addOnsTotal;
    }

    // Add event listeners
    Object.values(inputs).forEach(input => {
        if (input) {
            input.addEventListener('change', calculate);
            input.addEventListener('click', calculate);
        }
    });

    // Initial calculation
    calculate();
}

// ===================================
// FAQ Accordion
// ===================================
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', function() {
            const isActive = item.classList.contains('active');
            
            // Close all items
            faqItems.forEach(i => i.classList.remove('active'));
            
            // Open clicked item if it wasn't active
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
}

// ===================================
// Gallery
// ===================================
function initGallery() {
    const tabs = document.querySelectorAll('.gallery-tab');
    const items = document.querySelectorAll('.gallery-item');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');
            
            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Filter items
            items.forEach(item => {
                if (filter === 'all' || item.getAttribute('data-category') === filter) {
                    item.style.display = 'block';
                    item.style.animation = 'fadeInUp 0.5s ease forwards';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
}

// ===================================
// Contact Form
// ===================================
function initContactForm() {
    const form = document.getElementById('bookingForm');
    const messageDiv = document.getElementById('formMessage');

    if (!form) return;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Validate
        if (!validateForm(data)) {
            showMessage(messageDiv, 'Please fill in all required fields.', 'error');
            return;
        }

        // Simulate form submission
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        submitBtn.disabled = true;

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Success
        showMessage(messageDiv, 'Thank you! We\'ll contact you within 2 hours to confirm your booking.', 'success');
        form.reset();
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}

function validateForm(data) {
    const required = ['name', 'email', 'phone', 'date', 'service'];
    return required.every(field => data[field] && data[field].trim() !== '');
}

function showMessage(element, text, type) {
    element.textContent = text;
    element.className = 'form-message ' + type;
}

// ===================================
// Smooth Scroll
// ===================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                const navHeight = document.getElementById('navbar').offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===================================
// Scroll Animations
// ===================================
function initAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                fadeObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements with animation classes
    document.querySelectorAll('.feature-card, .service-card, .team-card, .area-card, .faq-item').forEach(el => {
        fadeObserver.observe(el);
    });

    // Parallax effect for hero
    window.addEventListener('scroll', function() {
        const hero = document.querySelector('.hero-bg');
        if (hero) {
            const scrolled = window.pageYOffset;
            hero.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });
}

// ===================================
// Utility Functions
// ===================================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
