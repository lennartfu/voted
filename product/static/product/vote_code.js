$(document).ready(function () {
    $('input[type="checkbox"]').change(function () {
        if (multiple_choice_allowed === "False") {
            $('input[type="checkbox"]').not(this).prop('checked', false);
        }
    });

    $(document).on('click', '.input-group-text-checkbox', function (event) {
        if ($(event.target).is('input[type="checkbox"]')) {
            return;
        }
        let checkbox = $(this).find('input[type="checkbox"]');
        checkbox.prop("checked", !checkbox.prop("checked")).change();
    });

    if (countDownDate) {
        const timer = $(".timer")

        function displayTime() {
            // Get today's date and time
            let now = new Date().getTime();
            // Find the distance between now and the countdown date
            let distance = countDownDate - now;
            // Time calculations for days, hours, minutes and seconds
            let days = Math.floor(distance / (1000 * 60 * 60 * 24));
            let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((distance % (1000 * 60)) / 1000);
            // Display the result in the element with id="timer"
            let timeString = "";
            if (days !== 0) timeString += days + "d";
            if (hours !== 0) timeString += " " + hours + "h";
            if (minutes !== 0) timeString += " " + minutes + "m";
            if (seconds !== 0) timeString += " " + seconds + "s";
            timer.text(timeString);
            // If the countdown is finished, write some text
            if (distance < 0) {
                timer.text("")
            }
        }

        displayTime();
        setInterval(displayTime, 1000);
    }
});
