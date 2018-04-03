// Run a single JSON fetch and update the HTML
function status_update() {
    return $.getJSON("status.json", function (data) {
        // Format & fill the amount of online users
        $("#steam_users").text(new Intl.NumberFormat().format(data.steam_users));

        // Fill the steam services
        $.each(data.steam_services, function (index, value) {
            if (value === 200)
                value = "online";
            else if (!isNaN(value))
                value = "HTTP Status Code " + value;

            $("#" + index).text(value);
        });

        // Fill the CS:GO services
        $.each(data.csgo_services, function (index, value) {
            $("#" + index).text(value);
        });

        // Fill the CS:GO servers
        $.each(data.csgo_servers, function (index, value) {
            index = index.toLowerCase().replace(/\s+/g, "_");
            $("#" + index).text(value);
        });
    })
    .done(function () {
        // Keywords to color the statuses differently
        var good_status = ["idle", "low", "normal", "online"];
        var okay_status = ["delayed", "medium"];
        var bad_status = ["high", "offline"];

        $(".status").each(function () {
            var text = $(this).text();
            if (good_status.includes(text))
                $(this).css("color", "#6C9541");
            else if (okay_status.includes(text))
                $(this).css("color", "#53A4C4");
            else if (bad_status.includes(text))
                $(this).css("color", "#F44336");
        });
    })
    .fail(function (jqXHR) {
        var status = jqXHR.status;
        var errmsg;
        if (status !== 0) {
            errmsg = "HTTP Status Code " + status + ": Check Flask for more details!";
        } else {
            errmsg = "Flask is not running!";
        }

        var servermsg = $("#servermsg");
        servermsg.addClass("alert-danger");
        servermsg.append(errmsg);
        servermsg.removeAttr("style");
    });
}

// Call status_update() every 45 seconds
function auto_update() {
    $.when(status_update()).done(function () {
        var start = new Date;
        var interval = setInterval(function () {
            var total_seconds = Math.floor((new Date - start) / 1000);
            var time_remaining = 45 - total_seconds;
            $('#seconds').text(time_remaining);

            if (time_remaining <= 0) {
                clearInterval(interval);
                auto_update();
            }
        }, 1000);
    });
}

// Calling auto_update() once to start the loop
$(document).ready(auto_update);
