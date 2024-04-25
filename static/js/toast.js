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