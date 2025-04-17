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
    const top =
      target.getBoundingClientRect().top + window.pageYOffset - offset;
    window.scrollTo({ top, behavior: "smooth" });
  }
}

// Function to toggle modal visibility
function toggleModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.classList.toggle("hidden");
}

// Function to send a message
function sendMessage() {
  const input = document.getElementById("chat-input");
  const chatContainer = document.getElementById("chat-container");

  if (input.value.trim() !== "") {
    // Add user message
    const userMessage = document.createElement("div");
    userMessage.className =
      "text-right text-sm text-primary bg-white p-2 rounded-md shadow-md";
    userMessage.textContent = input.value;
    chatContainer.appendChild(userMessage);

    // Simulate chatbot response
    setTimeout(() => {
      const botMessage = document.createElement("div");
      botMessage.className =
        "text-left text-sm text-primary bg-gray-100 p-2 rounded-md shadow-md";
      botMessage.textContent = "This is a response from the chatbot.";
      chatContainer.appendChild(botMessage);

      // Add Breakdown button
      const breakdownBtn = document.createElement("button");
      breakdownBtn.className = "mt-2 text-sm text-secondary hover:underline";
      breakdownBtn.textContent = "Breakdown";
      breakdownBtn.onclick = () => alert("Breakdown details...");
      chatContainer.appendChild(breakdownBtn);
    }, 1000);

    input.value = "";
  }
}

// Attach event listener to Chatbot feature card
document
  .querySelector('.feature-card[href="#"]')
  .addEventListener("click", (e) => {
    e.preventDefault();
    toggleModal("chatbot-modal");
  });

// Sample chat data (in a real app, this would come from a database)
const chatData = {
  "sleep-tracking": [
    { type: "user", text: "Hello, I need help with my sleep tracking." },
    {
      type: "bot",
      text: "Hi there! I'd be happy to help you with sleep tracking. What specific concerns do you have about your sleep patterns?",
      hasBreakdown: true,
    },
    {
      type: "user",
      text: "I've been having trouble falling asleep. Can you suggest some strategies?",
    },
    {
      type: "bot",
      text: "Of course! Here are some strategies that might help:<ul class='list-disc pl-6 mt-3 space-y-2'><li>Establish a regular sleep schedule</li><li>Create a relaxing bedtime routine</li><li>Limit screen time before bed</li><li>Keep your bedroom cool and dark</li></ul>Would you like more details on any of these?",
    },
  ],
  "diet-recommendations": [
    { type: "user", text: "I need help with my diet plan" },
    {
      type: "bot",
      text: "I'd be happy to help with your diet plan. What are your dietary goals?",
      hasBreakdown: true,
    },
    {
      type: "user",
      text: "I want to reduce sugar intake and eat more protein",
    },
    {
      type: "bot",
      text: "That's a great goal! Here are some suggestions:<ul class='list-disc pl-6 mt-3 space-y-2'><li>Replace sugary drinks with water or tea</li><li>Include lean protein at every meal</li><li>Read food labels for hidden sugars</li><li>Try Greek yogurt for a high-protein snack</li></ul>",
    },
  ],
  "exercise-routine": [
    { type: "user", text: "Can you recommend a home workout routine?" },
    {
      type: "bot",
      text: "Absolutely! What equipment do you have available at home?",
    },
    { type: "user", text: "Just a yoga mat and some resistance bands" },
    {
      type: "bot",
      text: "Perfect! Here's a 20-minute routine you can try:<ul class='list-disc pl-6 mt-3 space-y-2'><li>5-minute warm-up with dynamic stretches</li><li>Circuit: 30 seconds each of squats, push-ups, resistance band rows</li><li>Rest 1 minute, repeat circuit 3 times</li><li>5-minute cool down stretch</li></ul>",
      hasBreakdown: true,
    },
  ],
};

// Function to load chat messages
function loadChat(chatId) {
  const chatContainer = document.getElementById("chat-container");
  
  // Add fade-out animation before clearing
  chatContainer.classList.add('animate-fade-out');
  
  setTimeout(() => {
    chatContainer.innerHTML = ""; // Clear existing messages
    
    // Make previously selected chat item normal style
    document.querySelectorAll(".chat-history-item").forEach((item) => {
      item.classList.remove("bg-secondary");
      item.classList.add("bg-gray-200");
    });

    // Highlight the selected chat with transition
    const selectedItem = document.querySelector(`[data-chat-id="${chatId}"]`);
    if (selectedItem) {
      selectedItem.classList.remove("bg-gray-200");
      selectedItem.classList.add("bg-secondary", "transition-colors", "duration-300");
    }

    // Get the chat messages
    const messages = chatData[chatId];
    if (!messages) return;
    
    // Remove fade-out and add fade-in to container
    chatContainer.classList.remove('animate-fade-out');
    chatContainer.classList.add('animate-fade-in');

    // Add each message with a slight delay for animation
    messages.forEach((message, index) => {
      setTimeout(() => {
        const messageDiv = document.createElement("div");
        messageDiv.className = `flex justify-${
          message.type === "user" ? "end" : "start"
        } mb-6 opacity-0 transition-opacity duration-300`;

        const messageBubble = document.createElement("div");
        messageBubble.className =
          message.type === "user"
            ? "bg-primary text-white rounded-lg rounded-tr-sm shadow-lg max-w-lg px-6 py-4 transform transition-transform duration-300 scale-95"
            : "text-black bg-gray-200 rounded-lg rounded-tl-sm shadow-lg max-w-lg px-6 py-4 transform transition-transform duration-300 scale-95";
        messageBubble.innerHTML = message.text;

        messageDiv.appendChild(messageBubble);
        chatContainer.appendChild(messageDiv);

        // Add breakdown button if needed
        if (message.hasBreakdown) {
          const breakdownDiv = document.createElement("div");
          breakdownDiv.className = "flex justify-start mb-4 opacity-0 transition-opacity duration-300";

          const breakdownBtn = document.createElement("button");
          breakdownBtn.className =
            "text-xs text-primary bg-white px-4 py-2 rounded border border-primary hover:bg-primary hover:text-secondary transition-all duration-200 shadow-md";
          breakdownBtn.textContent = "Breakdown";
          breakdownBtn.onclick = () =>
            alert("Showing breakdown details for this response");

          breakdownDiv.appendChild(breakdownBtn);
          chatContainer.appendChild(breakdownDiv);
          
          // Animate breakdown button after short delay
          setTimeout(() => {
            breakdownDiv.classList.remove("opacity-0");
            breakdownDiv.classList.add("opacity-100");
          }, 100);
        }

        // Animate message appearance
        setTimeout(() => {
          messageDiv.classList.remove("opacity-0");
          messageDiv.classList.add("opacity-100");
          messageBubble.classList.remove("scale-95");
          messageBubble.classList.add("scale-100");
        }, 50);

        // Scroll to the bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }, index * 200); // Slightly faster staggered appearance
    });
    
    // Remove fade-in class after animation completes
    setTimeout(() => {
      chatContainer.classList.remove('animate-fade-in');
    }, 500);
    
  }, 300); // Wait for fade-out animation to complete
}

// Add event listeners to chat history items
document.querySelectorAll(".chat-history-item").forEach((item) => {
  item.addEventListener("click", function() {
    const chatId = this.getAttribute("data-chat-id");
    
    // Add ripple effect on click
    const ripple = document.createElement("span");
    ripple.classList.add("ripple-effect");
    this.appendChild(ripple);
    
    // Remove ripple after animation
    setTimeout(() => {
      ripple.remove();
    }, 600);
    
    loadChat(chatId);
  });
});

// Add CSS for animations if it doesn't exist already
if (!document.getElementById("chat-animations-css")) {
  const styleSheet = document.createElement("style");
  styleSheet.id = "chat-animations-css";
  styleSheet.textContent = `
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    @keyframes fadeOut {
      from { opacity: 1; }
      to { opacity: 0; }
    }
    .animate-fade-in {
      animation: fadeIn 0.3s ease-in-out forwards;
    }
    .animate-fade-out {
      animation: fadeOut 0.3s ease-in-out forwards;
    }
    .ripple-effect {
      position: absolute;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.7);
      transform: scale(0);
      animation: ripple 0.6s linear;
      pointer-events: none;
    }
    @keyframes ripple {
      to {
        transform: scale(4);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(styleSheet);
}

// Load the first chat by default
loadChat("sleep-tracking");
