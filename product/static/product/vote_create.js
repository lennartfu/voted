$(document).ready(function () {
    // select every second item input
    $('input[name^="option_"]').on('input', function () {
        // when the user enters a value, show the next 2 inputs
        if ($(this).val().trim() !== '') {
            $(this).closest('.visible').nextAll('.initial-hidden').slice(0, 2).addClass("visible").slideDown();
        }
    });

    // Event for changes to the "date_mode" select element
    $('#id_date_mode').on('change', function () {
        // Selected value
        var selectedValue = $(this).val();

        // Function to update "d-none" class and "required" attribute
        function updateVisibilityAndRequired(selector, show, required) {
            if (show) {
                selector.removeClass('d-none');
                selector.prop('required', required);
            } else {
                selector.addClass('d-none');
                selector.prop('required', false);
            }
        }

        // If "Date" is selected
        if (selectedValue === 'DATE') {
            // Hide time, show date
            updateVisibilityAndRequired($('label[for$="_time"]'), false, false);
            updateVisibilityAndRequired($('input[name$="_time"]'), false, false);
            updateVisibilityAndRequired($('label[for$="_date"]'), true, false);
            // First 2 are required
            updateVisibilityAndRequired($('input[name$="_date"]:lt(2)'), true, true);
            updateVisibilityAndRequired($('input[name$="_date"]:gt(1)'), true, false);
        }
        // If "Time" is selected
        else if (selectedValue === 'TIME') {
            // Hide date, show time
            updateVisibilityAndRequired($('label[for$="_date"]'), false, false);
            updateVisibilityAndRequired($('input[name$="_date"]'), false, false);
            updateVisibilityAndRequired($('label[for$="_time"]'), true, true);
            // First 2 are required
            updateVisibilityAndRequired($('input[name$="_time"]:lt(2)'), true, true);
            updateVisibilityAndRequired($('input[name$="_time"]:gt(1)'), true, false);
        }
        // If "Date & Time" is selected, show everything
        else {
            // Show time
            updateVisibilityAndRequired($('label[for$="_time"]'), true, true);
            // First 2 are required
            updateVisibilityAndRequired($('input[name$="_time"]:lt(2)'), true, true);
            updateVisibilityAndRequired($('input[name$="_time"]:gt(1)'), true, false);
            // Show date
            updateVisibilityAndRequired($('label[for$="_date"]'), true, true);
            // First 2 are required
            updateVisibilityAndRequired($('input[name$="_date"]:lt(2)'), true, true);
            updateVisibilityAndRequired($('input[name$="_date"]:gt(1)'), true, false);
        }
    });

    // Set the initial state based on the initially selected value
    $('#id_date_mode').trigger('change');
});
