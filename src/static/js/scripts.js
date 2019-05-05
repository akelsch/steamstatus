const COUNTDOWN_DURATION = 45;

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

    let interval = setInterval(() => {
        document.getElementById("countdown").textContent = seconds;

        if (--seconds < 0) {
            seconds = COUNTDOWN_DURATION;
            updateData();
        }
    }, 1000);
}

function handleData(data) {
    // Online Users
    let onlineUsers = new Intl.NumberFormat().format(data.steam.online)
    document.getElementById("online-users").textContent = onlineUsers;

    // Services I
    Object.entries(data.steam.services).forEach(([key, value]) => {
        key += "-status";

        if (value === 200) {
            value = "online";
        } else if (!isNaN(value)) {
            value = "HTTP Status Code " + value;
        }

        document.getElementById(key).textContent = value;
    });

    // Services II
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
    let serverMessage = document.getElementById("server-message");
    serverMessage.textContent = "Oops, something went wrong. Is Flask up and running?";
    serverMessage.removeAttribute("style");

    // TODO Stop countdown loop
}

function highlightData() {
    // Color palette
    const green = "#6C9541";
    const blue = "#53A4C4";
    const red = "#F44336";

    // Keywords to color statuses differently
    const goodStatus = ["idle", "low", "normal", "online"];
    const okayStatus = ["delayed", "medium"];
    const badStatus = ["high", "offline"];

    // Set color for every status class member
    document.querySelectorAll(".status").forEach(status => {
        const statusText = status.textContent;

        if (goodStatus.includes(statusText)) {
            status.style.color = green;
        } else if (okayStatus.includes(statusText)) {
            status.style.color = blue;
        } else if (badStatus.includes(statusText)) {
            status.style.color = red;
        }
    });
}
