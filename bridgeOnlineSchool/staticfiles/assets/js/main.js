(function() {
  "use strict";

  console.log('Main.js script loaded');

  // Wait for jQuery to be available and DOM to be ready
  $(document).ready(function() {
    console.log('jQuery ready, DOM loaded');
    
    /**
     * ============================================================================
     * CORE FUNCTIONALITY - GENERAL WEBSITE FEATURES
     * ============================================================================
     */

    /**
     * Apply .scrolled class to the body as the page is scrolled down
     */
    function toggleScrolled() {
      const $selectBody = $('body');
      const $selectHeader = $('#header');
      if (!$selectHeader.hasClass('scroll-up-sticky') && !$selectHeader.hasClass('sticky-top') && !$selectHeader.hasClass('fixed-top')) return;
      window.scrollY > 100 ? $selectBody.addClass('scrolled') : $selectBody.removeClass('scrolled');
    }

    $(document).on('scroll', toggleScrolled);
    $(window).on('load', toggleScrolled);

    /**
     * Mobile nav toggle - Optimized implementation with scroll lock
     */
    const $mobileNavToggleBtn = $('.mobile-nav-toggle');
    const $mobileNavMenu = $('.mobile-navmenu');
    const $mobileNavOverlay = $('.mobile-nav-overlay');
    const $mobileNavClose = $('.mobile-nav-close');
    let isMobileNavOpen = false;
    let scrollPosition = 0;

    function showMobileNav() {
      if ($mobileNavMenu.length && $mobileNavOverlay.length && !isMobileNavOpen) {
        // Save current scroll position
        scrollPosition = window.pageYOffset;
        
        // Add show animation classes
        $mobileNavMenu.addClass('mobile-nav-show');
        $mobileNavOverlay.addClass('mobile-nav-show');
        
        // Prevent body scroll and maintain position
        $('body').addClass('mobile-nav-active').css('top', `-${scrollPosition}px`);
        
        isMobileNavOpen = true;
        
        // Toggle hamburger icon
        $mobileNavToggleBtn.removeClass('bi-list').addClass('bi-x');
      }
    }

    function hideMobileNav() {
      if ($mobileNavMenu.length && $mobileNavOverlay.length && isMobileNavOpen) {
        // Remove show classes and add hide classes
        $mobileNavMenu.removeClass('mobile-nav-show');
        $mobileNavOverlay.removeClass('mobile-nav-show');
        $mobileNavMenu.addClass('mobile-nav-hide');
        $mobileNavOverlay.addClass('mobile-nav-hide');
        
        // After animation completes, remove hide classes to reset to default hidden state
        setTimeout(() => {
          $mobileNavMenu.removeClass('mobile-nav-hide');
          $mobileNavOverlay.removeClass('mobile-nav-hide');
        }, 300); // Match animation duration
        
        // Restore body scroll and position
        $('body').removeClass('mobile-nav-active').css('top', '');
        window.scrollTo(0, scrollPosition);
        
        isMobileNavOpen = false;
        
        // Reset hamburger icon
        $mobileNavToggleBtn.addClass('bi-list').removeClass('bi-x');
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
    if ($mobileNavToggleBtn.length) {
      $mobileNavToggleBtn.on('click', toggleMobileNav);
    }

    if ($mobileNavClose.length) {
      $mobileNavClose.on('click', hideMobileNav);
    }

    if ($mobileNavOverlay.length) {
      $mobileNavOverlay.on('click', hideMobileNav);
    }

    // Hide mobile nav when clicking on nav links
    if ($mobileNavMenu.length) {
      const $navLinks = $mobileNavMenu.find('.mobile-nav-list a');
      $navLinks.on('click', hideMobileNav);
    }

    /**
     * Toggle mobile nav dropdowns
     */
    $('.navmenu .toggle-dropdown').each(function() {
      $(this).on('click', function(e) {
        e.preventDefault();
        $(this).parent().toggleClass('active');
        $(this).parent().next().toggleClass('dropdown-active');
        e.stopImmediatePropagation();
      });
    });

    /**
     * Preloader
     */
    const $preloader = $('#preloader');
    if ($preloader.length) {
      $(window).on('load', () => {
        console.log('Window loaded, removing preloader');
        $preloader.remove();
      });
      
      // Fallback: Remove preloader after 3 seconds if window load doesn't fire
      setTimeout(() => {
        if ($preloader.length) {
          console.log('Fallback: Removing preloader after timeout');
          $preloader.remove();
        }
      }, 3000);
    }

    /**
     * Scroll top button
     */
    let $scrollTop = $('.scroll-top');

    function toggleScrollTop() {
      if ($scrollTop.length) {
        window.scrollY > 100 ? $scrollTop.addClass('active') : $scrollTop.removeClass('active');
      }
    }
    
    if ($scrollTop.length) {
      $scrollTop.on('click', (e) => {
        e.preventDefault();
        $('html, body').animate({
          scrollTop: 0
        }, 'smooth');
      });
    }

    $(window).on('load', toggleScrollTop);
    $(document).on('scroll', toggleScrollTop);

    /**
     * Animation on scroll function and init
     */
    function aosInit() {
      if (typeof AOS !== 'undefined') {
        AOS.init({
          duration: 600,
          easing: 'ease-in-out',
          once: true,
          mirror: false
        });
      }
    }
    $(window).on('load', aosInit);









    /**
     * Correct scrolling position upon page load for URLs containing hash links.
     */
    $(window).on('load', function(e) {
      if (window.location.hash) {
        if ($(window.location.hash).length) {
          setTimeout(() => {
            let $section = $(window.location.hash);
            let scrollMarginTop = $section.css('scrollMarginTop');
            $('html, body').animate({
              scrollTop: $section.offset().top - parseInt(scrollMarginTop)
            }, 'smooth');
          }, 100);
        }
      }
    });

    /**
     * Navmenu Scrollspy
     */
    let $navmenulinks = $('.navmenu a');
    let currentPosition = 0;
    let sections = [];

    $navmenulinks.each(function() {
      let $section = $($(this).attr('hash'));
      if ($section.length) {
        sections.push({
          id: $(this).attr('hash'),
          nav: $(this)
        });
      }
    });

    $(window).on('scroll', function() {
      let check = null;
      let current = '';

      sections.forEach(function(section) {
        let sectionTop = $(section.id).offset().top;
        let sectionHeight = $(section.id).height();
        if (window.scrollY >= (sectionTop - 265)) {
          current = section.nav.attr('href');
        }
      });

      $('.navmenu a.active').removeClass('active');
      $('.navmenu a[href="' + current + '"]').addClass('active');
    });

    /**
     * ============================================================================
     * AUTHENTICATION FUNCTIONALITY
     * ============================================================================
     */

    /**
     * Registration Form Validation
     */
    function initRegistrationValidation() {
      const $form = $('#registrationForm');
      if (!$form.length) return; // Exit if registration form is not on the page

      const $usernameField = $('#id_username');
      const $firstNameField = $('#id_first_name');
      const $lastNameField = $('#id_last_name');
      const $emailField = $('#id_email');
      const $password1Field = $('#id_password1');
      const $password2Field = $('#id_password2');

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
        const $errorDiv = $('<div>');
        $errorDiv.css('cssText', errorStyle);
        $errorDiv.text(message);
        return $errorDiv[0]; // Return DOM element for compatibility
      }

      function removeExistingErrors($field) {
        const $parent = $field.parent();
        $parent.find('.validation-error').remove();
      }

      function showError($field, message) {
        removeExistingErrors($field);
        const errorDiv = createErrorElement(message);
        $(errorDiv).addClass('validation-error');
        $field.parent().append(errorDiv);
        $field.css('borderColor', '#dc3545');
      }

      function clearError($field) {
        removeExistingErrors($field);
        $field.css('borderColor', '');
      }

      function validateUsername() {
        const value = $usernameField.val().trim();
        
        if (!value) {
          showError($usernameField, 'Username is required.');
          return false;
        }
        
        if (value.length > 50) {
          showError($usernameField, 'Username must be 50 characters or fewer.');
          return false;
        }
        
        if (!patterns.username.test(value)) {
          showError($usernameField, 'Username can only contain letters, digits, and underscores.');
          return false;
        }
        
        clearError($usernameField);
        return true;
      }

      function validateFirstName() {
        const value = $firstNameField.val().trim();
        
        if (!value) {
          showError($firstNameField, 'First name is required.');
          return false;
        }
        
        if (value.length > 100) {
          showError($firstNameField, 'First name must be 100 characters or fewer.');
          return false;
        }
        
        if (!patterns.name.test(value)) {
          showError($firstNameField, 'First name can only contain letters.');
          return false;
        }
        
        clearError($firstNameField);
        return true;
      }

      function validateLastName() {
        const value = $lastNameField.val().trim();
        
        if (!value) {
          showError($lastNameField, 'Last name is required.');
          return false;
        }
        
        if (value.length > 100) {
          showError($lastNameField, 'Last name must be 100 characters or fewer.');
          return false;
        }
        
        if (!patterns.name.test(value)) {
          showError($lastNameField, 'Last name can only contain letters.');
          return false;
        }
        
        clearError($lastNameField);
        return true;
      }

      function validateEmail() {
        const value = $emailField.val().trim();
        
        if (!value) {
          showError($emailField, 'Email is required.');
          return false;
        }
        
        if (!patterns.email.test(value)) {
          showError($emailField, 'Please enter a valid email address.');
          return false;
        }
        
        clearError($emailField);
        return true;
      }

      function validatePassword() {
        const value = $password1Field.val();
        
        if (!value) {
          showError($password1Field, 'Password is required.');
          return false;
        }
        
        if (value.length < 8) {
          showError($password1Field, 'Password must be at least 8 characters long.');
          return false;
        }
        
        if (!patterns.password.test(value)) {
          showError($password1Field, 'Password must contain letters, numbers, and special characters.');
          return false;
        }
        
        clearError($password1Field);
        return true;
      }

      function validatePasswordConfirmation() {
        const password1 = $password1Field.val();
        const password2 = $password2Field.val();
        
        if (!password2) {
          showError($password2Field, 'Password confirmation is required.');
          return false;
        }
        
        if (password1 !== password2) {
          showError($password2Field, 'Passwords do not match.');
          return false;
        }
        
        clearError($password2Field);
        return true;
      }

      // Real-time validation
      if ($usernameField.length) $usernameField.on('blur', validateUsername);
      if ($firstNameField.length) $firstNameField.on('blur', validateFirstName);
      if ($lastNameField.length) $lastNameField.on('blur', validateLastName);
      if ($emailField.length) $emailField.on('blur', validateEmail);
      if ($password1Field.length) $password1Field.on('blur', validatePassword);
      if ($password2Field.length) $password2Field.on('blur', validatePasswordConfirmation);

      // Validate password confirmation when password1 changes
      if ($password1Field.length && $password2Field.length) {
        $password1Field.on('input', function() {
          if ($password2Field.val()) {
            validatePasswordConfirmation();
          }
        });
      }

      // Form submission validation
      $form.on('submit', function(e) {
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
          const firstInvalidField = $form.find('input[style*="border-color: rgb(220, 53, 69)"]');
          if (firstInvalidField.length) {
            firstInvalidField.focus();
          }
        }
      });
    }

    /**
     * ============================================================================
     * USER PROFILE MANAGEMENT SYSTEM
     * ============================================================================
     * Handles user account settings, teacher profile creation, and form validation
     * for the Bridge Online School profile pages.
     */

    function initProfilePage() {
      if (!$('#settings-section').length && !$('#teacher-section').length) return;

      // Ensure jQuery dependency is loaded before initialization
      if (typeof $ === 'undefined') {
        setTimeout(initProfilePage, 100);
        return;
      }

      const $form = $('#settings-section form');
      const $confirmSaveBtn = $('#confirm-save-btn');
      const confirmChangesModal = new bootstrap.Modal($('#confirm-changes-modal')[0]);
      const $changesList = $('#changes-list');
      
      // Preserve original form values for change detection
      const originalValues = {
        first_name: window.profileData?.first_name || '',
        last_name: window.profileData?.last_name || '',
        email: window.profileData?.email || '',
        username: window.profileData?.username || ''
      };

      // Determines the currently active profile section
      function getCurrentSection() {
        const activeSection = $('.profile-section.active');
        if (activeSection.length) {
          return activeSection.attr('id').replace('-section', '');
        }
        return 'settings'; // Default to settings section
      }

      // Manages navigation between different profile sections
      function showSection(sectionName) {
        // Reset all navigation states to inactive
        $('.profile-nav-link').removeClass('active');
        $('.profile-section').removeClass('active');
        
        // Activate the requested section and corresponding navigation
        $(`.profile-nav-link[data-section="${sectionName}"]`).addClass('active');
        $(`#${sectionName}-section`).addClass('active');
      }

      // Binds click handlers to profile section navigation links
      $('.profile-nav-link').on('click', function(e) {
        e.preventDefault();
        const section = $(this).data('section');
        showSection(section);
      });

      // Restores previously active section from browser storage
      const savedSection = localStorage.getItem('profileActiveSection');
      if (savedSection) {
        showSection(savedSection);
        // Remove stored section data after successful restoration
        localStorage.removeItem('profileActiveSection');
      }

      // Displays contextual error messages within the profile interface
      function showAlert(message, section = 'account') {
        let $alertContainer = $('#settings-section');
        
        // Clear any previously displayed error notifications
        $alertContainer.find('.errorlist').remove();
        
        // Generate structured error message markup
        const errorHtml = `
          <ul class="errorlist">
            <li>${message}</li>
          </ul>
        `;
        
        // Position error message contextually based on section
        if (section === 'password') {
          $alertContainer.find('h5').after(errorHtml); // Password change section
        } else {
          $alertContainer.find('h3').after(errorHtml); // General account settings
        }
      }

      // Handle main form submission with validation
      if ($form.length) {
        $form.on('submit', function(e) {
          e.preventDefault();
          
          const formData = new FormData($form[0]);
          const firstName = formData.get('first_name');
          const lastName = formData.get('last_name');
          const email = formData.get('email');
          const username = formData.get('username');
          const newPassword = formData.get('new_password');
          const confirmPassword = formData.get('confirm_password');
          
          // Validate first name
          if (firstName && firstName.length > 100) {
            showAlert('First name must be 100 characters or fewer.', 'account');
            return;
          }
          if (firstName && !firstName.match(/^[a-zA-Z\s]+$/)) {
            showAlert('First name can only contain letters.', 'account');
            return;
          }
          
          // Validate last name
          if (lastName && lastName.length > 100) {
            showAlert('Last name must be 100 characters or fewer.', 'account');
            return;
          }
          if (lastName && !lastName.match(/^[a-zA-Z\s]+$/)) {
            showAlert('Last name can only contain letters.', 'account');
            return;
          }
          
          // Validate username
          if (username) {
            if (username.length > 50) {
              showAlert('Username must be 50 characters or fewer.', 'account');
              return;
            }
            if (username.length === 0) {
              showAlert('Username cannot be empty.', 'account');
              return;
            }
            if (!username.match(/^[a-zA-Z0-9_]+$/)) {
              showAlert('Username can only contain letters, digits, and underscores.', 'account');
              return;
            }
          }
          
          // Validate email format and length
          if (email) {
            if (email.length > 254) {
              showAlert('Email address is too long.', 'account');
              return;
            }
            if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
              showAlert('Please enter a valid email address.', 'account');
              return;
            }
          }
          
          // Validate password if provided
          if (newPassword) {
            // Check if passwords match
            if (newPassword !== confirmPassword) {
              showAlert('The two password fields didn\'t match.', 'password');
              return;
            }
            
            // Check password length
            if (newPassword.length < 8) {
              showAlert('Password must be at least 8 characters long.', 'password');
              return;
            }
            
            // Check password complexity: letters, numbers, and special characters
            const hasLetter = /[a-zA-Z]/.test(newPassword);
            const hasDigit = /\d/.test(newPassword);
            const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(newPassword);
            
            if (!hasLetter || !hasDigit || !hasSpecial) {
              showAlert('Password must contain letters, numbers, and special characters.', 'password');
              return;
            }
          }
          
          // Detect changes
          const changes = [];
          
          if (formData.get('first_name') !== originalValues.first_name) {
            changes.push({
              label: 'First Name',
              old: originalValues.first_name || '(empty)',
              new: formData.get('first_name') || '(empty)'
            });
          }
          
          if (formData.get('last_name') !== originalValues.last_name) {
            changes.push({
              label: 'Last Name',
              old: originalValues.last_name || '(empty)',
              new: formData.get('last_name') || '(empty)'
            });
          }
          
          if (formData.get('email') !== originalValues.email) {
            changes.push({
              label: 'Email',
              old: originalValues.email,
              new: formData.get('email')
            });
          }
          
          if (formData.get('username') !== originalValues.username) {
            changes.push({
              label: 'Username',
              old: originalValues.username,
              new: formData.get('username')
            });
          }
          
          if (newPassword) {
            changes.push({
              label: 'Password',
              old: '••••••••',
              new: '••••••••'
            });
          }
          
          // Display changes in modal
          if (changes.length > 0) {
            let changesHtml = '';
            changes.forEach(change => {
              changesHtml += `
                <div class="change-item">
                  <span class="change-label">New ${change.label}: ${change.new}</span>
                </div>
              `;
            });
            $changesList.html(changesHtml);
            $confirmSaveBtn.show();
            confirmChangesModal.show();
          } else {
            // No changes detected
            $changesList.html('<p class="text-muted mb-0"><i class="bi bi-info-circle me-2"></i>No changes detected.</p>');
            $confirmSaveBtn.hide();
            confirmChangesModal.show();
          }
        });
      }

      $confirmSaveBtn.on('click', function() {
        confirmChangesModal.hide();
        // Save current section to localStorage before form submission
        localStorage.setItem('profileActiveSection', getCurrentSection());
        // Submit the form without triggering the event listener again
        $form.off('submit');
        $form[0].submit();
      });

      // Handle Teacher Profile Form
      const $teacherForm = $('#teacher-section form');
      
      // Store original teacher profile values (these will be set by the template)
      const originalTeacherValues = {
        title: window.teacherProfileData?.title || '',
        experience: window.teacherProfileData?.experience || '',
        teaching_years: window.teacherProfileData?.teaching_years || '',
        lesson_price: window.teacherProfileData?.lesson_price || '',
        course_price: window.teacherProfileData?.course_price || '',
        avatar: window.teacherProfileData?.avatar || ''
      };

      // Function to show teacher alert messages
      function showTeacherAlert(message, field = '') {
        let $alertContainer = $('#teacher-section');
        
        // Remove existing error messages
        $alertContainer.find('.errorlist').remove();
        
        // Create error message HTML
        const errorHtml = `
          <ul class="errorlist">
            <li>${message}</li>
          </ul>
        `;
        
        // Insert error after the teacher profile title
        $alertContainer.find('h3').after(errorHtml);
      }

      if ($teacherForm.length) {
        $teacherForm.on('submit', function(e) {
          e.preventDefault();
          
          const formData = new FormData($teacherForm[0]);
          const title = formData.get('title');
          const experience = formData.get('experience');
          const teachingYears = formData.get('teaching_years');
          const lessonPrice = formData.get('lesson_price');
          const coursePrice = formData.get('course_price');
          const avatar = formData.get('avatar');
          
          // Validate title
          if (!title || title.trim() === '') {
            showTeacherAlert('Professional title is required.');
            return;
          }
          if (title.length > 50) {
            showTeacherAlert('Professional title must be 50 characters or fewer.');
            return;
          }
          
          // Validate experience
          if (!experience || experience.trim() === '') {
            showTeacherAlert('Professional teaching experience description is required.');
            return;
          }
          if (experience.length > 500) {
            showTeacherAlert('Experience description must be 500 characters or fewer.');
            return;
          }
          
          // Validate teaching years (optional field)
          if (teachingYears && (teachingYears < 0 || teachingYears > 99)) {
            showTeacherAlert('Teaching years must be between 0 and 99.');
            return;
          }
          
          // Validate lesson price
          if (!lessonPrice || lessonPrice === '') {
            showTeacherAlert('Lesson price is required.');
            return;
          }
          if (lessonPrice < 0 || lessonPrice > 999999) {
            showTeacherAlert('Lesson price must be between 0 and 999,999.');
            return;
          }
          
          // Validate course price
          if (!coursePrice || coursePrice === '') {
            showTeacherAlert('Course price is required.');
            return;
          }
          if (coursePrice < 0 || coursePrice > 9999999) {
            showTeacherAlert('Course price must be between 0 and 9,999,999.');
            return;
          }
          
          // Validate avatar (required for new profiles, optional for updates)
          const hasExistingProfile = originalTeacherValues.avatar !== '';
          if (!hasExistingProfile && (!avatar || avatar.name === '')) {
            showTeacherAlert('Profile picture is required.');
            return;
          }
          
          // Detect changes and submit
          localStorage.setItem('profileActiveSection', getCurrentSection());
          $teacherForm.off('submit');
          $teacherForm[0].submit();
        });
      }
    }

    /**
     * ============================================================================
     * SHOPPING CART FUNCTIONALITY
     * ============================================================================
     */

    /**
     * Shopping Cart Class for managing cart operations
     */
    class ShoppingCart {
      constructor() {
        this.storageKey = 'bridgeSchoolCart';
      }
      
      getCart() {
        const cart = localStorage.getItem(this.storageKey);
        return cart ? JSON.parse(cart) : {};
      }
      
      saveCart(cart) {
        localStorage.setItem(this.storageKey, JSON.stringify(cart));
        this.updateNavbarCount();
      }
      
      addItem(teacher) {
        const cart = this.getCart();
        const teacherId = teacher.id.toString();
        
        if (cart[teacherId]) {
          cart[teacherId].quantity += 1;
        } else {
          cart[teacherId] = {
            ...teacher,
            quantity: 1,
            notes: '',
            communication_method: ''
          };
        }
        
        this.saveCart(cart);
      }
      
      updateItem(teacherId, updates) {
        const cart = this.getCart();
        if (cart[teacherId]) {
          Object.assign(cart[teacherId], updates);
          this.saveCart(cart);
        }
      }
      
      removeItem(teacherId) {
        const cart = this.getCart();
        delete cart[teacherId];
        this.saveCart(cart);
      }
      
      getTotalItems() {
        const cart = this.getCart();
        return Object.values(cart).reduce((total, item) => total + item.quantity, 0);
      }
      
      getTotalPrice() {
        const cart = this.getCart();
        return Object.values(cart).reduce((total, item) => total + (item.lesson_price * item.quantity), 0);
      }
      
      updateNavbarCount() {
        const totalItems = this.getTotalItems();
        const $cartIconLink = $('#cart-icon-link');
        const $cartBadge = $('#cart-badge');
        
        if ($cartIconLink.length && $cartBadge.length) {
          $cartBadge.text(totalItems);
          $cartBadge.css('display', totalItems > 0 ? 'flex' : 'none');
          if (totalItems > 0) {
            $cartIconLink.css({
              'display': 'flex',
              'alignItems': 'center',
              'opacity': '1'
            });
          } else {
            $cartIconLink.css({
              'display': 'none',
              'opacity': '0'
            });
          }
        }
      }

      renderCart() {
        const cart = this.getCart();
        const cartItems = Object.values(cart);
        const $contentContainer = $('#cart-content');
        const $loading = $('#loading');
        
        // Hide loading
        if ($loading.length) $loading.css('display', 'none');
        
        // Update header count
        const $countElement = $('#cart-items-count');
        const totalItems = this.getTotalItems();
        if ($countElement.length) {
          $countElement.text(totalItems > 0 ? 
            `You have ${totalItems} lesson${totalItems !== 1 ? 's' : ''} in your cart` : 
            'Your cart is empty');
        }
        
        if (cartItems.length === 0) {
          // Show empty cart
          const $emptyTemplate = $('#empty-cart-template');
          if ($emptyTemplate.length && $contentContainer.length) {
            $contentContainer.html($emptyTemplate.html());
          }
        } else {
          // Show cart items
          const $cartTemplate = $('#cart-item-template');
          if ($cartTemplate.length && $contentContainer.length) {
            $contentContainer.html($cartTemplate.html());
            
            const $cartItemsList = $('#cart-items-list');
            if ($cartItemsList.length) {
              $cartItemsList.empty();
              
              cartItems.forEach(item => {
                $cartItemsList.append(this.createCartItemElement(item));
              });
            }
            
            this.updateSummary();
          }
        }
      }

      createCartItemElement(item) {
        const div = document.createElement('div');
        div.className = 'card shadow-sm border-0 mb-4 cart-item';
        div.setAttribute('data-teacher-id', item.id);
        
        div.innerHTML = `
          <div class="card-body p-4">
            <div class="row align-items-center">
              <!-- Teacher Avatar -->
              <div class="col-md-2 col-3 text-center mb-3 mb-md-0">
                <img src="${item.avatar_url}" alt="${item.first_name} ${item.last_name}" 
                     class="img-fluid rounded-circle" style="width: 80px; height: 80px; object-fit: cover;">
              </div>
              
              <!-- Teacher Info -->
              <div class="col-md-4 col-9 mb-3 mb-md-0">
                <h5 class="mb-1" style="color: var(--heading-color);">
                  ${item.first_name} ${item.last_name}
                </h5>
                <p class="text-muted mb-1">${item.title}</p>
                <small class="text-muted">$${item.lesson_price}/lesson</small>
              </div>
              
              <!-- Quantity Controls -->
              <div class="col-md-3 col-6 mb-3 mb-md-0">
                <label class="form-label small">Number of Lessons</label>
                <div class="input-group">
                  <button class="btn btn-outline-secondary btn-sm quantity-btn" type="button" data-action="decrease">
                    <i class="bi bi-dash"></i>
                  </button>
                  <input type="number" class="form-control text-center quantity-input" 
                         value="${item.quantity}" min="1" max="50">
                  <button class="btn btn-outline-secondary btn-sm quantity-btn" type="button" data-action="increase">
                    <i class="bi bi-plus"></i>
                  </button>
                </div>
              </div>
              
              <!-- Price & Remove -->
              <div class="col-md-2 col-6 text-end">
                <h6 class="mb-2 item-total" style="color: var(--accent-color);">
                  $<span class="total-amount">${(item.lesson_price * item.quantity).toFixed(2)}</span>
                </h6>
                <button class="btn btn-sm btn-outline-danger remove-item" title="Remove from cart">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
            
            <!-- Notes and Communication -->
            <div class="row mt-3">
              <div class="col-md-6 mb-3">
                <label class="form-label small">Important Notes for Teacher</label>
                <textarea class="form-control notes-input" rows="3" 
                          placeholder="Any specific topics, goals, or requirements...">${item.notes || ''}</textarea>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label small">Preferred Communication Method</label>
                <input type="text" class="form-control communication-input" 
                       placeholder="e.g., WhatsApp, Zoom, Email, Skype..."
                       value="${item.communication_method || ''}">
              </div>
            </div>
          </div>
        `;
        
        // Add event listeners
        this.addCartItemEventListeners(div);
        
        return div;
      }

      addCartItemEventListeners(element) {
        const teacherId = $(element).attr('data-teacher-id');
        
        // Quantity controls
        $(element).find('.quantity-btn').on('click', function(e) {
          const action = $(this).attr('data-action');
          const $quantityInput = $(element).find('.quantity-input');
          let quantity = parseInt($quantityInput.val());
          
          if (action === 'increase') {
            quantity += 1;
          } else if (action === 'decrease' && quantity > 1) {
            quantity -= 1;
          }
          
          $quantityInput.val(quantity);
          this.updateItem(teacherId, { quantity });
          this.updateItemDisplay(element, quantity);
          this.updateSummary();
        }.bind(this));
        
        // Manual quantity input
        $(element).find('.quantity-input').on('change', function(e) {
          const quantity = Math.max(1, parseInt($(this).val()) || 1);
          $(this).val(quantity);
          this.updateItem(teacherId, { quantity });
          this.updateItemDisplay(element, quantity);
          this.updateSummary();
        }.bind(this));
        
        // Notes input
        $(element).find('.notes-input').on('blur', function(e) {
          this.updateItem(teacherId, { notes: $(this).val() });
        }.bind(this));
        
        // Communication input
        $(element).find('.communication-input').on('blur', function(e) {
          this.updateItem(teacherId, { communication_method: $(this).val() });
        }.bind(this));
        
        // Remove button
        $(element).find('.remove-item').on('click', function() {
          if (confirm('Remove this teacher from your cart?')) {
            this.removeItem(teacherId);
            $(element).remove();
            this.updateSummary();
            
            // Check if cart is empty
            if (this.getTotalItems() === 0) {
              this.renderCart();
            }
          }
        }.bind(this));
      }

      updateItemDisplay(element, quantity) {
        const cart = this.getCart();
        const teacherId = $(element).attr('data-teacher-id');
        const item = cart[teacherId];
        
        if (item) {
          const $totalAmount = $(element).find('.total-amount');
          $totalAmount.text((item.lesson_price * quantity).toFixed(2));
        }
      }

      updateSummary() {
        const totalItems = this.getTotalItems();
        const totalPrice = this.getTotalPrice();
        
        const $totalItemsElement = $('#cart-total-items');
        const $totalPriceElement = $('#cart-total-price');
        
        if ($totalItemsElement.length) $totalItemsElement.text(totalItems);
        if ($totalPriceElement.length) $totalPriceElement.text(`$${totalPrice.toFixed(2)}`);
        
        // Update header
        const $countElement = $('#cart-items-count');
        if ($countElement.length) {
          $countElement.text(totalItems > 0 ? 
            `You have ${totalItems} lesson${totalItems !== 1 ? 's' : ''} in your cart` : 
            'Your cart is empty');
        }
      }
    }

    // Global cart instance
    window.shoppingCart = new ShoppingCart();

    /**
     * ============================================================================
     * TEACHER PAGE FUNCTIONALITY  
     * ============================================================================
     */

    function initTeacherPage() {
      console.log('DOM loaded, initializing teacher page functionality...');
      
      // Star rating functionality (for authenticated users)
      const $starButtons = $('.star-button');
      const $ratingValue = $('#ratingValue');
      const $selectedRatingDisplay = $('#selectedRatingDisplay');
      const $reviewForm = $('#reviewForm');
      
      // Only initialize star rating if elements exist (authenticated users only)
      if ($starButtons.length > 0 && $ratingValue.length) {
        console.log('Initializing star rating system...');
        let selectedRating = 0;
        
        // Function to update star display
        function updateStarDisplay(rating) {
          $starButtons.each(function() {
            const starRating = parseInt($(this).attr('data-rating'));
            if (starRating <= rating) {
              $(this).addClass('active');
            } else {
              $(this).removeClass('active');
            }
          });
        }
        
        // Click handler for each star
        $starButtons.each(function() {
          const rating = parseInt($(this).attr('data-rating'));
          
          $(this).on('click', function() {
            selectedRating = rating;
            $ratingValue.val(rating);
            $selectedRatingDisplay.text(rating + ' stars');
            updateStarDisplay(rating);
          });
          
          // Hover effects
          $(this).on('mouseenter', function() {
            updateStarDisplay(rating);
          });
          
          $(this).on('mouseleave', function() {
            updateStarDisplay(selectedRating);
          });
        });
        
        // Form submission
        if ($reviewForm.length) {
          $reviewForm.on('submit', function(e) {
            e.preventDefault();
            
            if (!selectedRating || selectedRating === 0) {
              alert('Please select a rating');
              return;
            }
            
            const formData = new FormData(this);
            const $submitBtn = $(this).find('button[type="submit"]');
            
            $submitBtn.prop('disabled', true).text('Submitting...');
            
            fetch($reviewForm.attr('action'), {
              method: 'POST',
              body: formData,
              headers: {
                'X-Requested-With': 'XMLHttpRequest',
              }
            })
            .then(response => response.json())
            .then(data => {
              if (data.success) {
                alert('Review submitted successfully!');
                location.reload();
              } else {
                alert(data.message || 'Error submitting review');
              }
            })
            .catch(error => {
              console.error('Error:', error);
              alert('Error submitting review');
            })
            .finally(() => {
              $submitBtn.prop('disabled', false).text('Submit Review');
            });
          });
        }
        
        // Reset when modal closes
        const $reviewModal = $('#reviewModal');
        if ($reviewModal.length) {
          $reviewModal.on('hidden.bs.modal', function() {
            selectedRating = 0;
            $ratingValue.val('');
            $selectedRatingDisplay.text('None');
            $starButtons.removeClass('active');
          });
        }
      }
      
      // Admin delete review functionality
      const $deleteButtons = $('.delete-review-btn');
      $deleteButtons.on('click', function() {
        const reviewId = $(this).attr('data-review-id');
        const teacherId = $(this).attr('data-teacher-id');
        
        if (confirm('Are you sure you want to delete this review?')) {
          fetch(`/admin/delete-review/${reviewId}/`, {
            method: 'POST',
            headers: {
              'X-Requested-With': 'XMLHttpRequest',
              'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
            }
          })
          .then(response => response.json())
          .then(data => {
            if (data.success) {
              location.reload();
            } else {
              alert(data.message || 'Error deleting review');
            }
          })
          .catch(error => {
            console.error('Error:', error);
            alert('Error deleting review');
          });
        }
      });
      
      // Add to Cart Functionality - Fixed for guest users
      function initializeCartFunctionality() {
        console.log('Initializing cart functionality...');
        
        const $cartButtons = $('.add-to-cart-btn');
        console.log('Found cart buttons:', $cartButtons.length);
        
        if ($cartButtons.length === 0) {
          console.warn('No cart buttons found on this page');
          return;
        }
        
        $cartButtons.each(function(index) {
          console.log(`Setting up cart button ${index + 1}`);
          
          // Remove any existing event listeners to prevent duplicates
          $(this).off('click', handleCartClick);
          
          // Add the click event listener
          $(this).on('click', handleCartClick);
        });
      }
      
      function handleCartClick(e) {
        e.preventDefault();
        e.stopPropagation();
        
        console.log('Cart button clicked!');
        
        try {
          // Check localStorage support
          if (typeof(Storage) === "undefined") {
            alert('Your browser does not support cart functionality. Please use a modern browser.');
            return;
          }
          
          // Get teacher data from button attributes
          const button = e.currentTarget;
          const teacherData = {
            id: parseInt(button.dataset.teacherId),
            first_name: button.dataset.teacherFirstname,
            last_name: button.dataset.teacherLastname,
            title: button.dataset.teacherTitle,
            lesson_price: parseFloat(button.dataset.teacherPrice),
            avatar_url: button.dataset.teacherAvatar
          };
          
          console.log('Teacher data:', teacherData);
          
          // Validate data
          if (!teacherData.id || !teacherData.first_name || isNaN(teacherData.id) || isNaN(teacherData.lesson_price)) {
            alert('Error: Invalid teacher information. Please refresh the page and try again.');
            return;
          }
          
          // Add item to cart using global cart instance
          window.shoppingCart.addItem(teacherData);
          
          // Show success message
          alert(`Added lesson with ${teacherData.first_name} ${teacherData.last_name} to your cart!`);
          
          // Redirect to cart page
          window.location.href = '/cart/';
          
        } catch (error) {
          console.error('Cart error:', error);
          alert('Error adding item to cart. Please try again.');
        }
      }
      
      // Initialize cart functionality immediately
      initializeCartFunctionality();
      
      // Also update cart display on page load
      window.shoppingCart.updateNavbarCount();
      

    }

    /**
     * ============================================================================
     * CART PAGE FUNCTIONALITY
     * ============================================================================
     */

    function initCartPage() {
      if (!$('#cart-content').length) return;

      // Initialize cart display
      window.shoppingCart.renderCart();
      
      // Check if teacher data was passed from server (non-AJAX add)
      const $teacherDataElement = $('#teacher-data');
      if ($teacherDataElement.length) {
        const teacherData = JSON.parse($teacherDataElement.text());
        window.shoppingCart.addItem(teacherData);
        window.shoppingCart.renderCart();
      }

      // Checkout functionality
      const $checkoutBtn = $('#proceed-checkout-btn');
      if ($checkoutBtn.length) {
        $checkoutBtn.on('click', function() {
          proceedToCheckout();
        });
      }

      // Handle pending checkout for users who logged in after adding items to cart
      if (window.DJANGO_CONFIG && window.DJANGO_CONFIG.isAuthenticated) {
        const pendingCheckout = localStorage.getItem('pendingCheckout');
        if (pendingCheckout) {
          try {
            const cartItems = JSON.parse(pendingCheckout);
            
            // Restore cart items to localStorage
            const cartData = {};
            cartItems.forEach(item => {
              cartData[item.id.toString()] = item;
            });
            localStorage.setItem('bridgeSchoolCart', JSON.stringify(cartData));
            
            // Clear pending checkout
            localStorage.removeItem('pendingCheckout');
            
            // Refresh cart display
            window.shoppingCart.renderCart();
            window.shoppingCart.updateNavbarCount();
            
          } catch (e) {
            console.error('Error restoring pending checkout:', e);
            localStorage.removeItem('pendingCheckout');
          }
        }
      }
    }

    function proceedToCheckout() {
      const cartData = window.shoppingCart.getCart();
      const cartItems = Object.values(cartData);
      
      if (cartItems.length === 0) {
        alert('Your cart is empty. Please add some lessons before checkout.');
        return;
      }
      
      // Check if user is authenticated
      if (window.DJANGO_CONFIG && window.DJANGO_CONFIG.isAuthenticated) {
        // User is authenticated, proceed to checkout form
        window.location.href = window.DJANGO_CONFIG.checkoutFormUrl;
      } else {
        // Guest user needs to login first
        if (confirm('You need to be logged in to complete your purchase. Would you like to sign in or sign up now?')) {
          // Save cart data to localStorage before redirect
          localStorage.setItem('pendingCheckout', JSON.stringify(cartItems));
          window.location.href = window.DJANGO_CONFIG.loginUrl + '?next=' + encodeURIComponent(window.DJANGO_CONFIG.checkoutFormUrl);
        }
      }
    }

    /**
     * ============================================================================
     * CHECKOUT FORM FUNCTIONALITY
     * ============================================================================
     */

    function initCheckoutForm() {
      if (!$('#checkoutForm').length) return;

      // Load cart data and populate order summary
      loadOrderSummary();
      
      // Pre-populate user data if available
      populateUserData();
      
      // Set up payment method switching
      setupPaymentMethods();
      
      // Set up form validation and submission
      setupFormSubmission();
      
      // Set up card number formatting
      setupCardFormatting();
    }

    function loadOrderSummary() {
      try {
        const cart = JSON.parse(localStorage.getItem('bridgeSchoolCart') || '{}');
        const cartItems = Object.values(cart);
        const $orderSummaryDiv = $('#orderSummary');
        
        if (cartItems.length === 0) {
          if ($orderSummaryDiv.length) {
            $orderSummaryDiv.html('<div class="alert alert-warning">Your cart is empty</div>');
          }
          const $completeOrderBtn = $('#completeOrderBtn');
          if ($completeOrderBtn.length) $completeOrderBtn.prop('disabled', true);
          return;
        }
        
        let summaryHtml = '';
        let totalItems = 0;
        let totalPrice = 0;
        
        cartItems.forEach(item => {
          const itemTotal = item.lesson_price * item.quantity;
          totalItems += item.quantity;
          totalPrice += itemTotal;
          
          summaryHtml += `
            <div class="order-item">
              <div class="d-flex align-items-center">
                <img src="${item.avatar_url}" alt="${item.first_name} ${item.last_name}" 
                     class="rounded-circle me-2" style="width: 40px; height: 40px; object-fit: cover;">
                <div class="flex-grow-1">
                  <h6 class="mb-0">${item.first_name} ${item.last_name}</h6>
                  <small class="text-muted">${item.quantity} lesson${item.quantity > 1 ? 's' : ''}</small>
                </div>
                <span class="fw-bold">$${itemTotal.toFixed(2)}</span>
              </div>
            </div>
          `;
        });
        
        if ($orderSummaryDiv.length) $orderSummaryDiv.html(summaryHtml);
        
        const $summaryTotalItems = $('#summaryTotalItems');
        const $summaryTotalPrice = $('#summaryTotalPrice');
        if ($summaryTotalItems.length) $summaryTotalItems.text(totalItems);
        if ($summaryTotalPrice.length) $summaryTotalPrice.text(`$${totalPrice.toFixed(2)}`);
        
      } catch (e) {
        console.error('Error loading order summary:', e);
        const $orderSummaryDiv = $('#orderSummary');
        if ($orderSummaryDiv.length) {
          $orderSummaryDiv.html('<div class="alert alert-danger">Error loading cart</div>');
        }
      }
    }

    function populateUserData() {
      if (window.CHECKOUT_CONFIG && window.CHECKOUT_CONFIG.userEmail) {
        const $emailField = $('#email');
        if ($emailField.length) $emailField.val(window.CHECKOUT_CONFIG.userEmail);
      }
      
      if (window.CHECKOUT_CONFIG && window.CHECKOUT_CONFIG.userName) {
        const nameParts = window.CHECKOUT_CONFIG.userName.split(' ');
        if (nameParts.length >= 1) {
          const $firstNameField = $('#firstName');
          if ($firstNameField.length) $firstNameField.val(nameParts[0]);
        }
        if (nameParts.length >= 2) {
          const $lastNameField = $('#lastName');
          if ($lastNameField.length) $lastNameField.val(nameParts.slice(1).join(' '));
        }
        const $cardNameField = $('#cardName');
        if ($cardNameField.length) $cardNameField.val(window.CHECKOUT_CONFIG.userName);
      }
    }

    function setupPaymentMethods() {
      const $paymentMethods = $('input[name="paymentMethod"]');
      const $creditCardDetails = $('#creditCardDetails');
      
      $paymentMethods.each(function() {
        $(this).on('change', function() {
          // Hide credit card details by default
          if ($creditCardDetails.length) $creditCardDetails.css('display', 'none');
          
          // Show credit card details only for credit card selection
          if ($(this).val() === 'credit_card' && $creditCardDetails.length) {
            $creditCardDetails.css('display', 'block');
          }
        });
        
        // Prevent clicking on disabled payment methods
        if ($(this).prop('disabled')) {
          $(this).closest('.payment-method-card').on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
          });
        }
      });
    }

    function setupCardFormatting() {
      // Format card number
      const $cardNumberInput = $('#cardNumber');
      if ($cardNumberInput.length) {
        $cardNumberInput.on('input', function() {
          let value = $(this).val().replace(/\s+/g, '').replace(/[^0-9]/gi, '');
          let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
          $(this).val(formattedValue);
        });
      }
      
      // Format expiry date
      const $expiryInput = $('#expiryDate');
      if ($expiryInput.length) {
        $expiryInput.on('input', function() {
          let value = $(this).val().replace(/\D/g, '');
          if (value.length >= 2) {
            value = value.substring(0, 2) + '/' + value.substring(2, 4);
          }
          $(this).val(value);
        });
      }
      
      // Format CVV
      const $cvvInput = $('#cvv');
      if ($cvvInput.length) {
        $cvvInput.on('input', function() {
          $(this).val($(this).val().replace(/\D/g, ''));
        });
      }
    }

    function setupFormSubmission() {
      const $form = $('#checkoutForm');
      if (!$form.length) return;
      
      $form.on('submit', function(e) {
        e.preventDefault();
        
        if (!this.checkValidity()) {
          e.stopPropagation();
          $(this).addClass('was-validated');
          return;
        }
        
        // Check if a disabled payment method is selected
        const $selectedPaymentMethod = $('input[name="paymentMethod"]:checked');
        if ($selectedPaymentMethod.length && $selectedPaymentMethod.prop('disabled')) {
          return;
        }
        
        // Show loading state
        const $submitBtn = $('#completeOrderBtn');
        if ($submitBtn.length) {
          const originalText = $submitBtn.html();
          $submitBtn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm me-2"></span>Processing...');
          
          // Simulate processing delay
          setTimeout(() => {
            processCheckout();
          }, 2000);
        }
      });
    }

    function processCheckout() {
      try {
        const cart = JSON.parse(localStorage.getItem('bridgeSchoolCart') || '{}');
        const cartItems = Object.values(cart);
        
        if (cartItems.length === 0) {
          alert('Your cart is empty');
          resetCheckoutButton();
          return;
        }
        
        // Get form data
        const $form = $('#checkoutForm');
        const formData = new FormData($form[0]);
        
        // Prepare checkout data
        const checkoutData = {
          items: cartItems.map(item => ({
            teacher_id: item.id,
            number_of_lessons: item.quantity,
            total_price: (item.lesson_price * item.quantity).toFixed(2),
            notes: item.notes || '',
            communication_method: item.communication_method || ''
          })),
          total_amount: Object.values(cart).reduce((total, item) => total + (item.lesson_price * item.quantity), 0).toFixed(2),
          billing_email: formData.get('email'),
          billing_name: `${formData.get('firstName')} ${formData.get('lastName')}`,
          payment_method: formData.get('paymentMethod'),
          transaction_id: `TXN_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
        };
        
        // Send AJAX request to create checkout
        fetch(window.CHECKOUT_CONFIG.createCheckoutUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val(),
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify(checkoutData)
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // Clear cart after successful processing
            localStorage.removeItem('bridgeSchoolCart');
            window.shoppingCart.updateNavbarCount();
            
            // Redirect to success page with checkout_id
            const successUrl = `${window.CHECKOUT_CONFIG.checkoutSuccessUrl}?checkout_id=${data.checkout_id}`;
            window.location.href = successUrl;
          } else {
            alert(data.message || 'Error processing checkout. Please try again.');
            resetCheckoutButton();
          }
        })
        .catch(error => {
          console.error('Checkout error:', error);
          alert('Error processing checkout. Please check your connection and try again.');
          resetCheckoutButton();
        });
        
      } catch (error) {
        console.error('Checkout error:', error);
        alert('Error processing checkout. Please try again.');
        resetCheckoutButton();
      }
    }
    
    function resetCheckoutButton() {
      const $submitBtn = $('#completeOrderBtn');
      if ($submitBtn.length) {
        $submitBtn.prop('disabled', false).html('<i class="bi bi-lock me-2"></i>Complete Order');
      }
    }

    /**
     * ============================================================================
     * CONTACT FORM FUNCTIONALITY
     * ============================================================================
     */

    function initContactForm() {
      const $contactForm = $('#contactForm');
      
      if ($contactForm.length) {
        $contactForm.on('submit', function(e) {
          e.preventDefault();
          
          if (!this.checkValidity()) {
            e.stopPropagation();
            $(this).addClass('was-validated');
            return;
          }
          
          // Show loading state
          const $submitBtn = $('#submitBtn');
          if ($submitBtn.length) {
            const originalText = $submitBtn.html();
            $submitBtn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm me-2"></span>Sending...');
            
            // Simulate form submission
            setTimeout(() => {
              alert('Thank you for your message! We\'ll get back to you within 24 hours.');
              $contactForm[0].reset();
              $contactForm.removeClass('was-validated');
              
              // Restore button
              $submitBtn.prop('disabled', false).html(originalText);
            }, 2000);
          }
        });
      }
    }

    /**
     * ============================================================================
     * HOME PAGE FUNCTIONALITY
     * ============================================================================
     */

    function initHomePage() {
      // Auto-scroll to teachers section after filtering
      const urlParams = new URLSearchParams(window.location.search);
      const hasFilters = urlParams.has('search') || urlParams.has('min_years') || 
                        urlParams.has('max_years') || urlParams.has('sort_by') || urlParams.has('has_reviews');
      
      if (hasFilters) {
        // Scroll to teachers section smoothly
        setTimeout(function() {
          const $teamSection = $('#team');
          if ($teamSection.length) {
            $teamSection[0].scrollIntoView({ 
              behavior: 'smooth',
              block: 'start'
            });
          }
        }, 100);
      }
      
      // Add event listener to clear button for immediate scroll
      const $clearBtn = $('.btn-clear[href*="landing:home"]');
      if ($clearBtn.length) {
        $clearBtn.on('click', function(e) {
          e.preventDefault();
          window.location.href = $(this).attr('href') + '#team';
        });
      }
    }

    /**
     * ============================================================================
     * INITIALIZATION - PAGE-SPECIFIC FUNCTIONALITY
     * ============================================================================
     */

    console.log('Starting page-specific initialization');

    // Initialize page-specific functionality when DOM is loaded
    // Initialize registration validation
    console.log('Initializing registration validation');
    initRegistrationValidation();
    
    // Initialize profile page functionality
    console.log('Initializing profile page');
    initProfilePage();
    
    // Initialize teacher page functionality  
    console.log('Checking for teacher page elements');
    if ($('.star-button').length || $('.add-to-cart-btn').length) {
      console.log('Initializing teacher page');
      initTeacherPage();
    }
    
    // Initialize cart page functionality
    console.log('Initializing cart page');
    initCartPage();
    
    // Initialize checkout form functionality
    console.log('Initializing checkout form');
    initCheckoutForm();
    
    // Initialize contact form functionality
    console.log('Initializing contact form');
    initContactForm();
    
    // Initialize home page functionality
    console.log('Initializing home page');
    initHomePage();
    
    // Update cart count on all pages
    console.log('Updating cart count');
    if (window.shoppingCart) {
      window.shoppingCart.updateNavbarCount();
    }

    console.log('Page initialization complete');

    /**
     * ============================================================================
     * GLOBAL CART COUNT UPDATE FUNCTION
     * ============================================================================
     */

    // Global function to update cart count (called from various places)
    window.updateCartCount = function() {
      if (window.shoppingCart) {
        window.shoppingCart.updateNavbarCount();
      }
    };

    console.log('jQuery document ready function completed successfully');

  });

})();