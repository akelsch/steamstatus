const COUNTDOWN_DURATION = 45;
let intervalId;

// Start update loop once the document is loaded
document.addEventListener("DOMContentLoaded", () => updateData().then(countdown));

async function updateData() {
    try {
        const response = await fetch("status.json");
        const data = await response.json();
        return handleData(data);
    } catch (error) {
        return handleError(error);
    }
}

function countdown() {
    let seconds = COUNTDOWN_DURATION;

    intervalId = setInterval(() => {
        document.getElementById("countdown").textContent = seconds;

        if (--seconds < 0) {
            seconds = COUNTDOWN_DURATION;
            updateData();
        }
    }, 1000);
}

function handleData(data) {
    // Steam Services
    document.getElementById("online-users").textContent = data.steam.online.toLocaleString();
    Object.entries(data.steam.services).forEach(([key, value]) => {
        key += "-status";

        if (value === 200) {
            value = "Normal";
        } else {
            value = "HTTP Status Code " + value;
        }

        document.getElementById(key).textContent = value;
    });

    // CS:GO Services
    document.getElementById("online-players").textContent = data.csgo.online.toLocaleString();
    Object.entries(data.csgo.services).forEach(([key, value]) => {
        key = key.replace(/_/g, "-");
        document.getElementById(key).textContent = value;
    });

    // CS:GO Servers
    Object.entries(data.csgo.servers).forEach(([key, value]) => {
        key = key.toLowerCase().replace(/ /g, "-");
        document.getElementById(key).textContent = value;
    });

    highlightData();
}

function handleError(error) {
    // Clear countdown interval
    clearInterval(intervalId);

    // Display error message
    const serverMessage = document.getElementById("server-message");
    serverMessage.textContent = "Oops, something went wrong. Is Flask up and running?";
    serverMessage.removeAttribute("style");
}

function highlightData() {
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
