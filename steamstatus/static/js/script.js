const COUNTDOWN_DURATION = 45;
let intervalId;

document.addEventListener("DOMContentLoaded", () => updateDocument().then(countdown));

function countdown() {
    let seconds = COUNTDOWN_DURATION;

    intervalId = setInterval(() => {
        document.getElementById("countdown").textContent = seconds;

        if (--seconds < 0) {
            seconds = COUNTDOWN_DURATION;
            updateDocument();
        }
    }, 1000);
}

async function updateDocument() {
    fetch("status.json")
        .then(response => response.json())
        .then(data => handleData(data))
        .catch(error => handleError(error))
        .then(highlightDocument);
}

function handleData(data) {
    // Steam Services
    document.getElementById("online-users").textContent = data.steam.online.toLocaleString();
    Object.entries(data.steam.services).forEach(([key, value]) => {
        document.getElementById(key).textContent = value == 200 ? "Normal" : "HTTP Status Code " + value;
    });

    // CS:GO Services
    document.getElementById("online-players").textContent = data.csgo.online.toLocaleString();
    Object.entries(data.csgo.services).forEach(([key, value]) => {
        document.getElementById(key).textContent = value;
    });

    // CS:GO Servers
    Object.entries(data.csgo.servers).forEach(([key, value]) => {
        key = key.toLowerCase().replace(/ /g, "-");
        document.getElementById(key).textContent = value;
    });
}

function handleError(error) {
    // Reset countdown
    clearInterval(intervalId);

    // Display error message
    const serverMessage = document.getElementById("errormsg");
    serverMessage.textContent = "Oops, something went wrong. Is Flask up and running?";
    serverMessage.removeAttribute("style");
}

function highlightDocument() {
    const statuses = {
        good: ["Idle", "Low", "Normal"],
        okay: ["Delayed", "Medium"],
        bad: ["Critical", "Full", "High", "Offline", "Surge"]
    };

    // Set color for every status class member
    document.querySelectorAll(".status").forEach(status => {
        const statusText = status.textContent;
        status.classList.toggle("good", statuses.good.includes(statusText));
        status.classList.toggle("okay", statuses.okay.includes(statusText));
        status.classList.toggle("bad", statuses.bad.includes(statusText));
    });
}
