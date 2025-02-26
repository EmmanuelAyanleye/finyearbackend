// Function to animate the counters when the section comes into view
const counters = document.querySelectorAll('.counters span');
const container = document.querySelector(".counters")

let activated = false;

window.addEventListener('scroll', () => {
  if (pageYOffset > container.offsetTop - container.offsetHeight - 200 && activated === false) {
    counters.forEach(counter => {
      counter.innerText = 0;
      let count = 0;

      function updateCount() {
        const target = parseInt(counter.dataset.count);

        if (count < target) {
          count++;

          counter.innerText = count;

          setTimeout(updateCount, 10);
        }else{
          counter.innerText = target;
        }
      }
      updateCount();
      activated = true;
    });
  }else if (pageYOffset < container.offsetTop - container.offsetHeight - 500 || pageYOffset === 0 && activated === true){
    counters.forEach(counter => {
      counter.innerText = 0;
    });
    activated = false;
  }
});




const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});


// Function to dynamically load a page
function loadPage(pageUrl) {
  // Fetch the content of the requested page
  fetch(pageUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to fetch the page content.');
      }
      return response.text();
    })
    .then(html => {
      // Replace the main content with the new page content
      document.getElementById('main-content').innerHTML = html;
    })
    .catch(error => {
      console.error('Error loading the page:', error);
      document.getElementById('main-content').innerHTML = `
        <div class="alert alert-danger" role="alert">
          Failed to load the page. Please try again later.
        </div>`;
    });
}
