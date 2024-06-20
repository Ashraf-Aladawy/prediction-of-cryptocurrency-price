document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");
  const signupForm = document.getElementById("signupForm");


  loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    try {
      const response = await fetch("/authenticate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
        credentials: "same-origin", // Use same-origin for cookies
      });

      if (response.ok) {
        // Redirect to dashboard or display success message
        window.location.href = "/dashboard.html";
      } else {
        const errorMessage = await response.text();
        alert(errorMessage); // Show error message to user
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again later.");
    }
  });

  signupForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("signupUsername").value;
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;

    try {
      const response = await fetch("http://localhost:5000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: username, email, password }),
        credentials: "include", // Include cookies
      });

      if (response.ok) {
        // Redirect to login page or display success message
        alert("User registered successfully. Please log in.");
        window.location.href = "/login.html";
      } else {
        const errorMessage = await response.text();
        alert(errorMessage); // Show error message to user
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again later.");
    }
  });

});
