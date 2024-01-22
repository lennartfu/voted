$(document).ready(function () {
    if (!final) {
        $(".tier-content")
            .sortable({
                connectWith: ".tier-content",
                placeholder: "placeholder",
                scrollSensitivity: 30,
                scrollSpeed: 100,
                start: function (e, ui) {
                    ui.placeholder.height(ui.item.height());
                    ui.placeholder.width(ui.item.width());
                }
            });
    }

    $(".btn-submit").click(function () {
        // JSON-Objekt erstellen
        var tierlistData = {
            "S": [],
            "A": [],
            "B": [],
            "C": [],
            "D": [],
            "E": [],
            "F": [],
            "none": []
        };

        // Durchlaufe jede Tierreihe und sammle die IDs der Vote-Items
        $(".tier-row").each(function () {
            var tierLabel = $(this).find(".tier-label").text().trim();
            var itemIDs = [];

            // Wenn es sich um das "none" Tier handelt
            if (tierLabel === "") {
                tierLabel = "none";
            }

            // Durchlaufe jedes Vote-Item in der aktuellen Tierreihe
            $(this).find(".tier-item").each(function () {
                var itemID = $(this).attr("id");
                itemIDs.push(parseInt(itemID));
            });

            // Füge die Liste der IDs dem JSON-Objekt hinzu
            tierlistData[tierLabel] = itemIDs;
        });

        $(".tier-content.last .tier-item").each(function () {
            var itemID = $(this).attr("id");
            tierlistData["none"].push(parseInt(itemID));
        });

        var requestBody = {
            "vote_data": tierlistData
        };

        console.log(requestBody)

        // POST-Request senden
        $.ajax({
            type: "POST",
            url: window.location.href,
            headers: {"X-CSRFToken": csrfToken},
            data: JSON.stringify(requestBody),
            contentType: "application/json",
            success: function (response) {
                location.reload();
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});
