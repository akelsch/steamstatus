// Start the loop once the document is loaded
document.addEventListener("DOMContentLoaded", startLoop);

// Call fetchUpdate() every x seconds
function startLoop() {
    fetchUpdate().then(function() {
        const x = 45;

        let start = new Date();
        let loop = setInterval(function() {
            let secondCount = Math.floor((new Date() - start) / 1000);
            let remainingTime = x - secondCount;

            document.querySelector("#countdown").innerHTML = remainingTime;

            if (remainingTime <= 0) {
                clearInterval(loop);
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
                // Pass HTTP status code in case of failure
                throw Error(response.status);
            }

            return response.json();
        }).then(function(json) {
            // ID: online-users
            document.querySelector("#online-users").innerHTML = new Intl.NumberFormat().format(json.steam.online);

            Object.entries(json.steam.services).forEach(([key, value]) => {
                if (value === 200) {
                    value = "online";
                } else if (!isNaN(value)) {
                    value = "HTTP Status Code " + value;
                }

                // IDs: store-status, community-status, api-status
                key += "-status";

                document.querySelector("#" + key).innerHTML = value;
            });

            Object.entries(json.csgo.services).forEach(([key, value]) => {
                // IDs: sessions-logon, player-inventories, matchmaking-scheduler
                key = key.replace(/_/g, "-");

                document.querySelector("#" + key).innerHTML = value;
            });

            Object.entries(json.csgo.servers).forEach(([key, value]) => {
                // IDs: australia, brazil, chile, china-guangzhou...
                key = key.toLowerCase().replace(/ /g, "-");

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
            document.querySelectorAll(".status").forEach(function(status) {
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
            console.log(error);

            let status = error.message;

            let errmsg;
            if (!isNaN(status)) {
                errmsg = "HTTP Status Code " + status + ": Check Flask for more details!";
            } else {
                errmsg = "Oops, something went wrong. Is Flask up and running?";
            }

            let servermsg = document.querySelector("#servermsg");
            servermsg.innerHTML = errmsg;
            servermsg.removeAttribute("style");
        });
}
