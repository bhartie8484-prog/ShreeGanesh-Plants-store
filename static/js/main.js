// Flash message close functionality
document.addEventListener("DOMContentLoaded", function () {
  const authModalOverlay = document.querySelector(".auth-modal-overlay");
  const authModalClose = document.querySelector(".auth-modal-close");
  if (authModalOverlay && authModalClose) {
    authModalClose.addEventListener("click", () => {
      authModalOverlay.classList.add("is-hidden");
    });
  }

  document.querySelectorAll(".password-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const input = document.getElementById(button.dataset.passwordTarget);
      if (!input) return;
      const showing = input.type === "text";
      input.type = showing ? "password" : "text";
      button.setAttribute("aria-label", showing ? "Show password" : "Hide password");
      button.querySelector("i").className = showing ? "fas fa-eye" : "fas fa-eye-slash";
    });
  });

  // Mobile navigation
  const navToggle = document.querySelector(".nav-toggle");
  const navMenu = document.querySelector(".nav-menu");

  if (navToggle && navMenu) {
    const closeNavigation = () => {
      navMenu.classList.remove("is-open");
      navToggle.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.setAttribute("aria-label", "Open navigation menu");
    };

    navToggle.addEventListener("click", () => {
      const isOpen = navMenu.classList.toggle("is-open");
      navToggle.classList.toggle("is-open", isOpen);
      navToggle.setAttribute("aria-expanded", String(isOpen));
      navToggle.setAttribute(
        "aria-label",
        isOpen ? "Close navigation menu" : "Open navigation menu",
      );
    });

    navMenu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeNavigation);
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeNavigation();
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 768) closeNavigation();
    });
  }

  // Close flash messages
  const flashCloseButtons = document.querySelectorAll(".flash-close");
  flashCloseButtons.forEach((button) => {
    button.addEventListener("click", function () {
      this.parentElement.style.animation = "slideOut 0.3s ease";
      setTimeout(() => {
        this.parentElement.style.display = "none";
      }, 300);
    });
  });

  // Auto-hide flash messages after 5 seconds
  const flashMessages = document.querySelectorAll(".flash");
  flashMessages.forEach((flash) => {
    setTimeout(() => {
      flash.style.animation = "slideOut 0.3s ease";
      setTimeout(() => {
        flash.style.display = "none";
      }, 300);
    }, 5000);
  });


  // Add to cart animation
  const addToCartButtons = document.querySelectorAll('a[href*="add_to_cart"]');
  addToCartButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      // Create animation effect
      const cart = document.querySelector('.nav-menu a[href*="cart"]');
      if (cart) {
        cart.style.animation = "cartBounce 0.5s ease";
        setTimeout(() => {
          cart.style.animation = "";
        }, 500);
      }
    });
  });

  // Product card hover effects - enhance with scale
  const productCards = document.querySelectorAll(
    ".modern-product-card, .product-card",
  );
  productCards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transition = "all 0.3s ease";
    });
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Navbar scroll effect
  let lastScroll = 0;
  const navbar = document.querySelector(".navbar");

  window.addEventListener("scroll", function () {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
      navbar.style.boxShadow = "0 4px 16px rgba(0,0,0,0.12)";
    } else {
      navbar.style.boxShadow = "0 2px 8px rgba(0,0,0,0.08)";
    }

    lastScroll = currentScroll;
  });

  // Form validation with better UX
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    const inputs = form.querySelectorAll("input[required], textarea[required]");

    inputs.forEach((input) => {
      input.addEventListener("blur", function () {
        if (!this.value.trim()) {
          this.style.borderColor = "#f44336";
        } else {
          this.style.borderColor = "#68b984";
        }
      });

      input.addEventListener("focus", function () {
        this.style.borderColor = "#68b984";
      });
    });

    form.addEventListener("submit", function (e) {
      let isValid = true;

      inputs.forEach((input) => {
        if (!input.value.trim()) {
          isValid = false;
          input.style.borderColor = "#f44336";
          input.focus();
        }
      });

      if (!isValid) {
        e.preventDefault();
        showNotification("Please fill in all required fields", "error");
      }
    });
  });

  // Image lazy loading fallback with placeholder
  const images = document.querySelectorAll("img");
  images.forEach((img) => {
    img.addEventListener("load", function () {
      this.style.opacity = "1";
    });

    img.addEventListener("error", function () {
      // Already handled by onerror in HTML
      this.style.opacity = "1";
    });
  });

  // Quick View functionality (if product detail modal needed in future)
  const quickViewBtns = document.querySelectorAll(".quick-view-btn");
  quickViewBtns.forEach((btn) => {
    btn.addEventListener("click", function (e) {
      // For now, just navigate to detail page
      // In future, can show modal instead
    });
  });

  // Price formatting helper
  const priceElements = document.querySelectorAll(
    ".current-price, .product-price, .item-price",
  );
  priceElements.forEach((element) => {
    // Already formatted in template, but can add formatting here if needed
  });

  console.log("🌿 PlantStore - Website loaded successfully!");
  console.log("Modern UI with Nurserylive-inspired design");
});

// Add slide out animation to CSS dynamically
const style = document.createElement("style");
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    @keyframes cartBounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
`;
document.head.appendChild(style);

// Helper function to format currency
function formatCurrency(amount) {
  return (
    "₹" +
    parseFloat(amount).toLocaleString("en-IN", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    })
  );
}

// Helper function to show notifications
function showNotification(message, type = "info") {
  const notification = document.createElement("div");
  notification.className = `flash flash-${type}`;
  notification.style.animation = "slideIn 0.3s ease";
  notification.innerHTML = `
        ${message}
        <button class="flash-close">&times;</button>
    `;

  let container = document.querySelector(".flash-container");
  if (!container) {
    container = createFlashContainer();
  }
  container.appendChild(notification);

  // Auto-hide
  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease";
    setTimeout(() => notification.remove(), 300);
  }, 5000);

  // Close button
  notification.querySelector(".flash-close").addEventListener("click", () => {
    notification.style.animation = "slideOut 0.3s ease";
    setTimeout(() => notification.remove(), 300);
  });
}

function createFlashContainer() {
  const container = document.createElement("div");
  container.className = "flash-container";
  document.body.appendChild(container);
  return container;
}
