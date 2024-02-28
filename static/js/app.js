//timeout the pop-up success and error messages upon user action

var message_timeout = document.getElementById("timed-message");

setTimeout(function ()

    {
        message_timeout.style.display = "none";
    }, 5000);