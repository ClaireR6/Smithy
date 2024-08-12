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
const characterRace = parseInt(data.characterrace, 10)
const characterId = parseInt(data.characterid, 10)

function setRace(raceId, characterId) {
    $.ajax({
            type: "POST",
            url: "/dbRace/",
            data: {action: "set", race_id: raceId, character_id: characterId},
            success: function () {
                window.location.reload()
            },
            error: reporterr
        }
    )
}

function toggleArrow(id) {
    $("#icon" + id).toggleClass("fa-caret-down")
    $("#icon" + id).toggleClass("fa-caret-right")
}

function showSelect(){
    $("#raceSelect").toggleClass("d-none")
}

// Fills race information on page
function fill(data) {
    if (data) {
        let infoHtml = "";
        if (data.raceInfo.raceId !== characterRace) {
            infoHtml += "<h3 class=\"yellow d-flex flex-row h-100 align-items-center\"> " + data.raceInfo.raceName + " <button class=\'btn btn-success ms-auto\' onclick=\'setRace(" + data.raceInfo.raceId + ", " + characterId + ")\'> Confirm </button></h3>\n"
        } // <button class=\'btn btn-success ms-auto\' onclick=\'addClass(" + data.classInfo.classId + ", "+characterId+")\'> Add Class </button>
        else {
            infoHtml += "<h3 class=\"yellow\"> " + data.raceInfo.raceName + " </h3>\n"
        }

        const traits = data.traits
        infoHtml += "<div id=\"accordion\">"
        traits.forEach(function (trait) {
            infoHtml +=
                "<div class=\"card bg-transparent border-0\">" +
                "<div class=\"card-header border-0\" id=\"heading" + data.raceInfo.raceId + "" + trait.traitId + "\">" +
                // "<h5 class=\"mb-0\">" +
                "<button class=\"d-flex flex-row p-0 btn btn-lg w-100 yellow collapseBtnYlw text-start border-0\" data-bs-toggle=\"collapse\" data-bs-target=\"#collapse" + data.raceInfo.raceId + "" + trait.traitId + "\"" +
                "aria-expanded=\"true\" aria-controls=\"collapse" + data.raceInfo.raceId + "" + trait.traitId + "\" onclick=\'toggleArrow(" + data.raceInfo.raceId + "" + trait.traitId + ")\'>" +
                "<p class=\'me-auto\'> " + trait.name + " </p>" +
                "<i id=\"icon" + data.raceInfo.raceId + "" + trait.traitId + "\" class=\"fa fa-caret-down yellow ms-auto\"></i>" +
                "</button>" +
                // "</h5>" +
                "</div>" +
                "<div id=\"collapse" + data.raceInfo.raceId + "" + trait.traitId + "\" class=\"collapse border-0\" aria-labelledby=\"heading" + data.raceInfo.raceId + "" + trait.traitId + "\"" +
                "data-parent=\"#accordion\">" +
                "<div class=\"card-body greyText\">" +
                // "<hr class=\'border-5 opacity-100 mb-3 mt-0 yellow\' >" +
                trait.description +
                "</div>" +
                "</div>" +
                "</div>";
        })
        infoHtml += "</div>";
        $("#raceInfo").html(infoHtml)
    }
    else{
        $("#raceInfo").html("")
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


    $("#raceSelect").change(function () {

        let raceId = $("#raceSelect").val()

        if (raceId !== "unselected") {
            // send race id, get race information
            $.ajax({
                    type: "POST",
                    url: "/dbRace/",
                    data: {action: "get", race_id: raceId},
                    success: fill,
                    error: reporterr
                }
            )
        } else if (characterRace != null) {
            $.ajax({
                    type: "POST",
                    url: "/dbRace/",
                    data: {action: "get", race_id: characterRace},
                    success: fill,
                    error: reporterr
                }
            )
        } else {
            $("#raceInfo").html("")
        }
    });
});

