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

// Fills race information on page
function fill(data) {
    if (data) {
        let infoHtml = "";
        infoHtml +=
            "<h3 class=\"yellow\"> " + data.raceName + " </h3>\n" +
            "<hr class=\"yellow my-3 border-3 opacity-100\">" +
            "<h4 class=\"yellow\"> Ability Score Increases</h4>\n" +
            "<p class=\"greyText\"> There's info that goes here </p>\n" +
            "<h4 class=\"yellow\"> Speed </h4>\n" +
            "<p class=\"greyText\"> Your walking speed is " + data.speed + "</p>";


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

    $("#raceSelect").change(function () {

        const raceId = $("#raceSelect").val()

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
        } else {
            $("#raceInfo").html("")
        }
    });
});

