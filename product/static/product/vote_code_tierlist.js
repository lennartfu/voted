$(".tier-content")
    .sortable({
        connectWith: ".tier-content",
        placeholder: "placeholder",
        scrollSensitivity: 30,
        scrollSpeed: 100,
        start: function (e, ui) {
            ui.placeholder.height(ui.item.height());
            ui.placeholder.width(ui.item.width());
        },
        stop: function (e, ui) {
            let itemID = ui.item.attr("id");
            let tierID = ui.item.parent().prev().attr("id");
            saveData(itemID, tierID);
        }
    });
