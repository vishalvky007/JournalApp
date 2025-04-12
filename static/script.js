// Modal functionality
document.addEventListener("DOMContentLoaded", function () {

  // "Get Started" button opens login modal
  document
    .getElementById("get-started-btn")
    .addEventListener("click", function () {
      document.getElementById("login-modal").classList.remove("hidden");
    });

  // Login modal
  document.getElementById("login-btn").addEventListener("click", function () {
    document.getElementById("login-modal").classList.remove("hidden");
  });

  // Register modal open
  document
    .getElementById("register-btn")
    .addEventListener("click", function () {
      document.getElementById("register-modal").classList.remove("hidden");
    });

  // Common modal close logic (for both login & register)
  document.querySelectorAll(".modal-close").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".modal").forEach((modal) => {
        modal.classList.add("hidden");
      });
    });
  });

  // Close modals
  const modalCloseButtons = document.querySelectorAll(".modal-close");
  modalCloseButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      document.querySelectorAll(".modal").forEach(function (modal) {
        modal.classList.add("hidden");
      });
    });
  });

  // Close modal when clicking outside
  const modals = document.querySelectorAll(".modal");
  modals.forEach(function (modal) {
    modal.addEventListener("click", function (e) {
      if (e.target === modal) {
        modal.classList.add("hidden");
      }
    });
  });

  // Smooth scroll for anchor links
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href");
      const targetElement = document.querySelector(targetId);

      if (targetElement) {
        const offsetTop =
          targetElement.getBoundingClientRect().top + window.pageYOffset;
        window.scrollTo({
          top: offsetTop - 70,
          behavior: "smooth",
        });
      }
    });
  });

  // Feature card hover effect
  const featureCards = document.querySelectorAll(".feature-card");
  featureCards.forEach(function (card) {
    card.addEventListener("mouseenter", function () {
      this.querySelector("h3").classList.add("text-primary");
    });

    card.addEventListener("mouseleave", function () {
      this.querySelector("h3").classList.remove("text-primary");
    });
  });
});


function scrollToWithOffset(id, offset = 100) {
  const target = document.getElementById(id);
  if (target) {
    const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
    window.scrollTo({ top, behavior: 'smooth' });
  }
}