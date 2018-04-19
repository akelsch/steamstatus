// Start the loop once the document is loaded
document.addEventListener("DOMContentLoaded", startLoop);

// Call fetchUpdate() every x seconds
function startLoop() {
    fetchUpdate().then(function() {
        const x = 45;

        let start = new Date;
        let interval = setInterval(function() {
            let sum = Math.floor((new Date - start) / 1000);
            let remaining = x - sum;

            document.querySelector("#seconds").innerHTML = remaining;

            if (remaining <= 0) {
                clearInterval(interval);
                startLoop();
            }
        }, 1000);
    });
}

// Run a single JSON fetch and update the document
function fetchUpdate() {
    return fetch("status.json")
        .then(function(response) {
            if (!response.ok) {
                throw Error(response.status);
            }

            return response.json();
        }).then(function(json) {
            // Online users
            document.querySelector("#steam_users").innerHTML = new Intl.NumberFormat().format(json.steam_users);

            // Services
            Object.entries(json.steam_services).forEach(([key, value]) => {
                if (value === 200) {
                    value = "online";
                } else if (!isNaN(value)) {
                    value = "HTTP Status Code " + value;
                }

                document.querySelector("#" + key).innerHTML = value;
            });

            Object.entries(json.csgo_services).forEach(([key, value]) => {
                document.querySelector("#" + key).innerHTML = value;
            });

            // CS:GO servers
            Object.entries(json.csgo_servers).forEach(([key, value]) => {
                // Regex: Replace whitespaces with underscore
                key = key.toLowerCase().replace(/\s+/g, "_");

                document.querySelector("#" + key).innerHTML = value;
            });
        }).then(function() {
            // Keywords to color the statuses differently
            let goodStatus = ["idle", "low", "normal", "online"];
            let okayStatus = ["delayed", "medium"];
            let badStatus = ["high", "offline"];

            // Color palette
            let green = "#6C9541";
            let blue = "#53A4C4";
            let red = "#F44336";

            // Set color for every status class member
            // Reference: https://css-tricks.com/snippets/javascript/loop-queryselectorall-matches/
            let statuses = document.querySelectorAll(".status");
            [].forEach.call(statuses, function(status) {
                let statusText = status.innerHTML;

                if (goodStatus.includes(statusText)) {
                    status.style.color = green;
                } else if (okayStatus.includes(statusText)) {
                    status.style.color = blue;
                } else if (badStatus.includes(statusText)) {
                    status.style.color = red;
                }
            });
        }).catch(function(error) {
            let status = error.message;

            let errmsg;
            if (!isNaN(status)) {
                errmsg = "HTTP Status Code " + status + ": Check Flask for more details!";
            } else {
                errmsg = "Flask is not running!";
            }

            let servermsg = document.querySelector("#servermsg");
            servermsg.innerHTML = errmsg;
            servermsg.removeAttribute("style");
        });
}
