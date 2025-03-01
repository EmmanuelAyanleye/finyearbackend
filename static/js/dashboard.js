const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});


window.addEventListener('DOMContentLoaded', function () {
  const messages = document.querySelectorAll('.message'); // Get all messages
  
  // Loop through each message and add the 'show' class
  messages.forEach(function (message) {
      message.classList.add('show');  // Show the message
      
      // Set a timer to remove the 'show' class after 5 seconds
      setTimeout(function () {
          message.classList.remove('show');
      }, 5000); // Adjust time as needed (in milliseconds)
  });
});