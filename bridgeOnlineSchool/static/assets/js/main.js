/**
* Template Name: Consulting
* Template URL: https://bootstrapmade.com/bootstrap-consulting-website-template/
* Updated: May 01 2025 with Bootstrap v5.3.5
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobile nav toggle - Optimized implementation with scroll lock
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');
  const mobileNavMenu = document.querySelector('.mobile-navmenu');
  const mobileNavOverlay = document.querySelector('.mobile-nav-overlay');
  const mobileNavClose = document.querySelector('.mobile-nav-close');
  let isMobileNavOpen = false;
  let scrollPosition = 0;

  function showMobileNav() {
    if (mobileNavMenu && mobileNavOverlay && !isMobileNavOpen) {
      // Save current scroll position
      scrollPosition = window.pageYOffset;
      
      // Add show animation classes
      mobileNavMenu.classList.add('mobile-nav-show');
      mobileNavOverlay.classList.add('mobile-nav-show');
      
      // Prevent body scroll and maintain position
      document.body.classList.add('mobile-nav-active');
      document.body.style.top = `-${scrollPosition}px`;
      
      isMobileNavOpen = true;
      
      // Toggle hamburger icon
      mobileNavToggleBtn.classList.remove('bi-list');
      mobileNavToggleBtn.classList.add('bi-x');
    }
  }

  function hideMobileNav() {
    if (mobileNavMenu && mobileNavOverlay && isMobileNavOpen) {
      // Remove show classes and add hide classes
      mobileNavMenu.classList.remove('mobile-nav-show');
      mobileNavOverlay.classList.remove('mobile-nav-show');
      mobileNavMenu.classList.add('mobile-nav-hide');
      mobileNavOverlay.classList.add('mobile-nav-hide');
      
      // After animation completes, remove hide classes to reset to default hidden state
      setTimeout(() => {
        mobileNavMenu.classList.remove('mobile-nav-hide');
        mobileNavOverlay.classList.remove('mobile-nav-hide');
      }, 300); // Match animation duration
      
      // Restore body scroll and position
      document.body.classList.remove('mobile-nav-active');
      document.body.style.top = '';
      window.scrollTo(0, scrollPosition);
      
      isMobileNavOpen = false;
      
      // Reset hamburger icon
      mobileNavToggleBtn.classList.add('bi-list');
      mobileNavToggleBtn.classList.remove('bi-x');
    }
  }

  function toggleMobileNav() {
    if (isMobileNavOpen) {
      hideMobileNav();
    } else {
      showMobileNav();
    }
  }

  // Event listeners
  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', toggleMobileNav);
  }

  if (mobileNavClose) {
    mobileNavClose.addEventListener('click', hideMobileNav);
  }

  if (mobileNavOverlay) {
    mobileNavOverlay.addEventListener('click', hideMobileNav);
  }

  // Hide mobile nav when clicking on nav links
  if (mobileNavMenu) {
    const navLinks = mobileNavMenu.querySelectorAll('.mobile-nav-list a');
    navLinks.forEach(navLink => {
      navLink.addEventListener('click', hideMobileNav);
    });
  }

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /*
   * Pricing Toggle
   */

  const pricingContainers = document.querySelectorAll('.pricing-toggle-container');

  pricingContainers.forEach(function(container) {
    const pricingSwitch = container.querySelector('.pricing-toggle input[type="checkbox"]');
    const monthlyText = container.querySelector('.monthly');
    const yearlyText = container.querySelector('.yearly');

    pricingSwitch.addEventListener('change', function() {
      const pricingItems = container.querySelectorAll('.pricing-item');

      if (this.checked) {
        monthlyText.classList.remove('active');
        yearlyText.classList.add('active');
        pricingItems.forEach(item => {
          item.classList.add('yearly-active');
        });
      } else {
        monthlyText.classList.add('active');
        yearlyText.classList.remove('active');
        pricingItems.forEach(item => {
          item.classList.remove('yearly-active');
        });
      }
    });
  });

  /**
   * Frequently Asked Questions Toggle
   */
  document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle').forEach((faqItem) => {
    faqItem.addEventListener('click', () => {
      faqItem.parentNode.classList.toggle('faq-active');
    });
  });

  /**
   * Correct scrolling position upon page load for URLs containing hash links.
   */
  window.addEventListener('load', function(e) {
    if (window.location.hash) {
      if (document.querySelector(window.location.hash)) {
        setTimeout(() => {
          let section = document.querySelector(window.location.hash);
          let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
          window.scrollTo({
            top: section.offsetTop - parseInt(scrollMarginTop),
            behavior: 'smooth'
          });
        }, 100);
      }
    }
  });

  /**
   * Navmenu Scrollspy
   */
  let navmenulinks = document.querySelectorAll('.navmenu a');

  function navmenuScrollspy() {
    navmenulinks.forEach(navmenulink => {
      if (!navmenulink.hash) return;
      let section = document.querySelector(navmenulink.hash);
      if (!section) return;
      let position = window.scrollY + 200;
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        document.querySelectorAll('.navmenu a.active').forEach(link => link.classList.remove('active'));
        navmenulink.classList.add('active');
      } else {
        navmenulink.classList.remove('active');
      }
    })
  }
  window.addEventListener('load', navmenuScrollspy);
  document.addEventListener('scroll', navmenuScrollspy);

  /**
   * Registration Form Validation
   */
  function initRegistrationValidation() {
    const form = document.getElementById('registrationForm');
    if (!form) return; // Exit if registration form is not on the page

    const usernameField = document.getElementById('id_username');
    const firstNameField = document.getElementById('id_first_name');
    const lastNameField = document.getElementById('id_last_name');
    const emailField = document.getElementById('id_email');
    const password1Field = document.getElementById('id_password1');
    const password2Field = document.getElementById('id_password2');

    // Validation patterns
    const patterns = {
      username: /^[a-zA-Z0-9_]+$/, // Letters, digits and underscore only
      name: /^[a-zA-Z\s]+$/, // Only letters and spaces
      email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, // Basic email pattern
      password: /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/ // 8+ chars, letters, numbers, special chars
    };

    // Error message styles
    const errorStyle = 'color: #dc3545; font-size: 0.875em; margin-top: 0.25rem;';

    function createErrorElement(message) {
      const errorDiv = document.createElement('div');
      errorDiv.style.cssText = errorStyle;
      errorDiv.textContent = message;
      return errorDiv;
    }

    function removeExistingErrors(field) {
      const parent = field.parentElement;
      const existingErrors = parent.querySelectorAll('.validation-error');
      existingErrors.forEach(error => error.remove());
    }

    function showError(field, message) {
      removeExistingErrors(field);
      const errorDiv = createErrorElement(message);
      errorDiv.classList.add('validation-error');
      field.parentElement.appendChild(errorDiv);
      field.style.borderColor = '#dc3545';
    }

    function clearError(field) {
      removeExistingErrors(field);
      field.style.borderColor = '';
    }

    function validateUsername() {
      const value = usernameField.value.trim();
      
      if (!value) {
        showError(usernameField, 'Username is required.');
        return false;
      }
      
      if (value.length > 50) {
        showError(usernameField, 'Username must be 50 characters or fewer.');
        return false;
      }
      
      if (!patterns.username.test(value)) {
        showError(usernameField, 'Username can only contain letters, digits, and underscores.');
        return false;
      }
      
      clearError(usernameField);
      return true;
    }

    function validateFirstName() {
      const value = firstNameField.value.trim();
      
      if (!value) {
        showError(firstNameField, 'First name is required.');
        return false;
      }
      
      if (value.length > 100) {
        showError(firstNameField, 'First name must be 100 characters or fewer.');
        return false;
      }
      
      if (!patterns.name.test(value)) {
        showError(firstNameField, 'First name can only contain letters.');
        return false;
      }
      
      clearError(firstNameField);
      return true;
    }

    function validateLastName() {
      const value = lastNameField.value.trim();
      
      if (!value) {
        showError(lastNameField, 'Last name is required.');
        return false;
      }
      
      if (value.length > 100) {
        showError(lastNameField, 'Last name must be 100 characters or fewer.');
        return false;
      }
      
      if (!patterns.name.test(value)) {
        showError(lastNameField, 'Last name can only contain letters.');
        return false;
      }
      
      clearError(lastNameField);
      return true;
    }

    function validateEmail() {
      const value = emailField.value.trim();
      
      if (!value) {
        showError(emailField, 'Email is required.');
        return false;
      }
      
      if (!patterns.email.test(value)) {
        showError(emailField, 'Please enter a valid email address.');
        return false;
      }
      
      clearError(emailField);
      return true;
    }

    function validatePassword() {
      const value = password1Field.value;
      
      if (!value) {
        showError(password1Field, 'Password is required.');
        return false;
      }
      
      if (value.length < 8) {
        showError(password1Field, 'Password must be at least 8 characters long.');
        return false;
      }
      
      if (!patterns.password.test(value)) {
        showError(password1Field, 'Password must contain letters, numbers, and special characters.');
        return false;
      }
      
      clearError(password1Field);
      return true;
    }

    function validatePasswordConfirmation() {
      const password1 = password1Field.value;
      const password2 = password2Field.value;
      
      if (!password2) {
        showError(password2Field, 'Password confirmation is required.');
        return false;
      }
      
      if (password1 !== password2) {
        showError(password2Field, 'Passwords do not match.');
        return false;
      }
      
      clearError(password2Field);
      return true;
    }

    // Real-time validation
    usernameField.addEventListener('blur', validateUsername);
    firstNameField.addEventListener('blur', validateFirstName);
    lastNameField.addEventListener('blur', validateLastName);
    emailField.addEventListener('blur', validateEmail);
    password1Field.addEventListener('blur', validatePassword);
    password2Field.addEventListener('blur', validatePasswordConfirmation);

    // Validate password confirmation when password1 changes
    password1Field.addEventListener('input', function() {
      if (password2Field.value) {
        validatePasswordConfirmation();
      }
    });

    // Form submission validation
    form.addEventListener('submit', function(e) {
      const isUsernameValid = validateUsername();
      const isFirstNameValid = validateFirstName();
      const isLastNameValid = validateLastName();
      const isEmailValid = validateEmail();
      const isPasswordValid = validatePassword();
      const isPasswordConfirmationValid = validatePasswordConfirmation();

      if (!isUsernameValid || !isFirstNameValid || !isLastNameValid || 
          !isEmailValid || !isPasswordValid || !isPasswordConfirmationValid) {
        e.preventDefault();
        
        // Focus on first invalid field
        const firstInvalidField = form.querySelector('input[style*="border-color: rgb(220, 53, 69)"]');
        if (firstInvalidField) {
          firstInvalidField.focus();
        }
      }
    });
  }

  // Initialize registration validation when DOM is loaded
  document.addEventListener('DOMContentLoaded', initRegistrationValidation);

})();