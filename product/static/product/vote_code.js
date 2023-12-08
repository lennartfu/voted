$(document).ready(function () {
    if (countDownDate) {
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
            $(".timer").text(days + "d " + hours + "h "
                + minutes + "m " + seconds + "s ");
            // If the countdown is finished, write some text
            if (distance < 0) {
                $(".timer").text("Zeit abgelaufen.")
            }
        }

        $('input[type="checkbox"]').change(function () {
            if (multiple_choice_allowed === "False") {
                $('input[type="checkbox"]').not(this).prop('checked', false);
            }
        });

        displayTime();
        setInterval(displayTime, 1000);
    }
});

