function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function makeToast(message, status) {
    // console.log("message = " + message);
    // console.log("status = " + status);
    var toast = document.getElementById("toast");
    var bgColor = "";
    if (status == 200) {
        bgColor = "bg-success";
        toast.classList.remove("bg-danger");
    } else if (status == 400) {
        bgColor = "bg-danger";
        toast.classList.remove("bg-success");
    }
    // console.log("bgcolor = " + bgColor);
    toast.classList.add(bgColor)

    var toastBody = toast.querySelector('.toast-body');

    // Set the message
    toastBody.textContent = message;

    // Show the toast
    var bootstrapToast = new bootstrap.Toast(toast);
    bootstrapToast.show();

    setTimeout(function () {
        if (status == 200) {
            bootstrapToast.hide();
            toast.classList.remove(bgColor);
            toastBody.textContent = "";
        }
    }, 4000);
}
document.getElementById('registrationForm').addEventListener('submit', function (event) {
    event.preventDefault();

    // Collect form data
    const formData = {
        username: this.elements.username.value,
        email: this.elements.email.value,
        password1: this.elements.password1.value,
        password2: this.elements.password2.value
    };

    // Send form data using fetch post request
    fetch('/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Function to get CSRF token
        },
        body: JSON.stringify(formData)
    })
        .then(response => {
            if (response.ok) {
                console.log("User Created");
                return response.json();
            } else {
                return response.json().then(data => Promise.reject(data));
            }
        })
        .then(data => {
            makeToast(data.message, 200);
            setTimeout(function () {
                window.location.href = "/signin";
            }, 4000); // 3000 milliseconds = 3 seconds
        })
        .catch(error => {
            console.error('Error:', error);
            let errorMessage = typeof error.message === 'object' ? Object.values(error.message).join(" ") : error.message;
            makeToast(errorMessage, 400);
        });
});