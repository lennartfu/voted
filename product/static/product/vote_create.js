$(document).ready(function () {
    // select every second item input
    $('input[name^="item_"]:odd').on('input', function () {
        // when the user enters a value, show the next 2 inputs
        if ($(this).val().trim() !== '') {
            $(this).closest('.visible').nextAll('.initial-hidden').slice(0, 2).addClass("visible").slideDown();
        }
    });
});