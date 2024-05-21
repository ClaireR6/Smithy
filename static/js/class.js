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

function addClass(classId, characterId) {
    $.ajax({
            type: "POST",
            url: "/dbClass/",
            data: {action: "add", class_id: classId, character_id: characterId},
            error: reporterr
        }
    )
}

// Fills race information on page
function fill(data) {
    if (data) {
        let infoHtml = "";
        infoHtml +=
            "<h3 class=\"yellow d-flex\"> " + data.classInfo.name + "<button class=\'btn btn-success ms-auto\' onclick=\'addClass(" + data.classInfo.classId + ", "+characterId+")\'> Add Class </button> </h3>\n" +
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
                "<button class=\"d-flex flex-row p-0 btn btn-lg w-100 yellow collapseBtn text-start border-0\" data-bs-toggle=\"collapse\" data-bs-target=\"#collapse" + data.classInfo.classId + "" + feat.featId + "\"" +
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
    }

}

function reporterr(data) {
    console.log(data.error)
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
                    data: {action: "get", class_id: charClassId},
                    success: fill,
                    error: reporterr
                }
            )
        } else {
            $("#classInfo").html("")
        }
    });
});

