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
    const serverMessage = document.getElementById("server-message");
    serverMessage.textContent = "Oops, something went wrong. Is Flask up and running?";
    serverMessage.removeAttribute("style");
}

function highlightDocument() {
    const statuses = {
        bad: {
            color: "#F44336", // red
            keywords: ["Offline", "High"]
        },
        okay: {
            color: "#53A4C4", // blue
            keywords: ["Delayed", "Medium"],
        },
        good: {
            color: "#6C9541", // green
            keywords: ["Idle", "Normal", "Low"]
        }
    }

    // Set color for every status class member
    document.querySelectorAll(".status").forEach(status => {
        const statusText = status.textContent;

        if (statuses.bad.keywords.includes(statusText)) {
            status.style.color = statuses.bad.color;
        } else if (statuses.okay.keywords.includes(statusText)) {
            status.style.color = statuses.okay.color;
        } else if (statuses.good.keywords.includes(statusText)) {
            status.style.color = statuses.good.color;
        }
    });
}
