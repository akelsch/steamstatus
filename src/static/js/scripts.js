// Start the loop once the document is loaded
document.addEventListener("DOMContentLoaded", startLoop);

/**
 * Calls fetchUpdate() every x seconds.
 */
function startLoop() {
    const x = 45;

    fetchUpdate()
        .then(function() {
            let secondCount = 0;

            const loop = setInterval(function() {
                secondCount++;
                let remainingTime = x - secondCount;

                document.querySelector("#countdown").innerHTML = remainingTime;

                if (remainingTime <= 0) {
                    clearInterval(loop);
                    startLoop();
                }
            }, 1000);
        }).catch(function(error) {
            // Reset the countdown
            document.querySelector("#countdown").innerHTML = x;
        });
}

/**
 * Runs a single JSON fetch and updates the document.
 */
async function fetchUpdate() {
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
            const goodStatus = ["idle", "low", "normal", "online"];
            const okayStatus = ["delayed", "medium"];
            const badStatus = ["high", "offline"];

            // Color palette
            const green = "#6C9541";
            const blue = "#53A4C4";
            const red = "#F44336";

            // Set color for every status class member
            document.querySelectorAll(".status").forEach(function(status) {
                const statusText = status.innerHTML;

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

            const status = error.message;

            let errmsg;
            if (!isNaN(status)) {
                errmsg = "HTTP Status Code " + status + ": Check Flask for more details!";
            } else {
                errmsg = "Oops, something went wrong. Is Flask up and running?";
            }

            const servermsg = document.querySelector("#servermsg");
            servermsg.innerHTML = errmsg;
            servermsg.removeAttribute("style");

            // Stop the loop
            return Promise.reject();
        });
}
