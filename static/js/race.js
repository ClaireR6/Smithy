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

// Fills race information on page
function fill(data) {
    if (data) {
        let infoHtml = "";
        if (data.raceInfo.raceId !== characterRace) {
            infoHtml += "<h3 class=\"yellow d-flex flex-row h-100 align-items-center\"> " + data.raceInfo.raceName + " <button class=\'btn btn-success ms-auto\' onclick=\'setRace(" + data.raceInfo.raceId + ", " + characterId + ")\'> Set Race </button></h3>\n"
        } // <button class=\'btn btn-success ms-auto\' onclick=\'addClass(" + data.classInfo.classId + ", "+characterId+")\'> Add Class </button>
        else {
            infoHtml += "<h3 class=\"yellow\"> " + data.raceInfo.raceName + " </h3>\n"
        }
        infoHtml +=
            "<hr class=\"yellow my-3 border-3 opacity-100\">" +
            "<h4 class=\"yellow\"> Ability Score Increases</h4>\n" +
            "<p class=\"greyText\"> There's info that goes here </p>\n" +
            "<h4 class=\"yellow\"> Speed </h4>\n" +
            "<p class=\"greyText\"> Your walking speed is " + data.raceInfo.speed + "</p>";


        const traits = data.traits
        traits.forEach(function (trait) {
            infoHtml +=
                "<h4 class=\"yellow\"> " + trait.name + " </h4>\n" +
                "<p class=\"greyText\"> " + trait.description + " </p>";
        })
        $("#raceInfo").html(infoHtml)
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

    changed()

    function changed() {

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
    }

    $("#raceSelect").change(function () {
        changed()
    });
});

