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
    var toast = document.getElementById("toast");
    var bgColor = "";
    if (status == 200) {
        bgColor = "bg-success";
    } else if (status == 400) {
        bgColor = "bg-danger";
    }
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

const data = document.currentScript.dataset;
const characterId = parseInt(data.characterid, 10)

function accordionToggle(id) {
    document.querySelectorAll(".collapse").forEach(function (element) {
        if (element.id !== "collapse" + id && element.classList.contains("show")) {
            element.classList.toggle("show")
        }
    })
}

function toggleArrow(id) {
    $("#icon" + id).toggleClass("fa-caret-down")
    $("#icon" + id).toggleClass("fa-caret-right")
}

// Fills class information on page
function fill(data) {
    if (data) {
        let infoHtml = "";
        infoHtml +=
            "<h3 class=\"yellow d-flex flex-row h-100 align-items-center\"> " + data.classInfo.name + "<button class=\'btn btn-success ms-auto\' onclick=\'addClass(" + data.classInfo.classId + ")\'> Add Class </button> </h3>\n" +
            "<hr class=\"yellow my-3 border-3 opacity-100\">";

        const feats = data.features
        // feats.forEach(function (feat) {
        //     infoHtml +=
        //         "<h4 class=\"yellow card-header\"> " + feat.name + " </h4>" +
        //         "<div class=\"greyText\"> " + feat.description + " </div>";
        // })
        infoHtml += "<div id=\"accordion\">"
        feats.forEach(function (feat) {
            infoHtml +=
                "<div class=\"card bg-transparent border-0\">" +
                "<div class=\"card-header border-0\" id=\"heading" + data.classInfo.classId + "" + feat.featId + "\">" +
                // "<h5 class=\"mb-0\">" +
                "<button class=\"d-flex flex-row p-0 btn btn-lg w-100 yellow collapseBtnYlw text-start border-0\" data-bs-toggle=\"collapse\" data-bs-target=\"#collapse" + data.classInfo.classId + "" + feat.featId + "\"" +
                "aria-expanded=\"true\" aria-controls=\"collapse" + data.classInfo.classId + "" + feat.featId + "\" onclick=\'toggleArrow(" + data.classInfo.classId + "" + feat.featId + ")\'>" +
                "<p class=\'me-auto\'> " + feat.name + " </p>" +
                "<i id=\"icon" + data.classInfo.classId + "" + feat.featId + "\" class=\"fa fa-caret-down yellow ms-auto\"></i>" +
                "</button>" +
                // "</h5>" +
                "</div>" +
                "<div id=\"collapse" + data.classInfo.classId + "" + feat.featId + "\" class=\"collapse border-0\" aria-labelledby=\"heading" + data.classInfo.classId + "" + feat.featId + "\"" +
                "data-parent=\"#accordion\">" +
                "<div class=\"card-body greyText\">" +
                // "<hr class=\'border-5 opacity-100 mb-3 mt-0 yellow\' >" +
                feat.description +
                "</div>" +
                "</div>" +
                "</div>";
        })
        infoHtml += "</div>";
        $("#classInfo").html(infoHtml)
    } else {
        $("#classInfo").html("")

    }

}

function reporterr(error) {
    console.error('Error:', error);
    let errorMessage = typeof error.message === 'object' ? Object.values(error.message).join(" ") : error.message;
    makeToast(errorMessage, 400);
}

function addClass(classId) {
    $.ajax({
            type: "POST",
            url: "/dbClass/",
            data: {action: "add", class_id: classId, character_id: characterId},
            success: function () {
                window.location.reload()
            },
            error: reporterr
        }
    )
}
$(function () //ready function
{
    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrftoken
        }
    });

    $("#classSelect").change(function () {

        const charClassId = $("#classSelect").val()

        if (charClassId !== "unselected") {
            // send race id, get race information
            $.ajax({
                    type: "POST",
                    url: "/dbClass/",
                    data: {action: "get", class_id: charClassId, character_id: characterId},
                    success: fill,
                    error: reporterr
                }
            )
        } else {
            $("#classInfo").html("")
        }
    });

    $("#classLvlContainer").on('change', '.classLvl-select', function () {
        const classLvlId = $(this).data("classlvlid")
        const lvl = $(this).val()
        $.ajax({
                type: "POST",
                url: "/dbClass/",
                data: {action: "level", character_id: characterId, classlvl_id: classLvlId, level: lvl},
                success: function () {
                    window.location.reload()
                },
                error: reporterr
            }
        )
    });

    $(".remove-class").click(function () {
        const classLvlId = $(this).data("classlvlid")
        $.ajax({
                type: "POST",
                url: "/dbClass/",
                data: {action: "remove", character_id: characterId, classlvl_id: classLvlId},
                success: function () {
                    window.location.reload()
                },
                error: reporterr
            }
        )
    });
});

