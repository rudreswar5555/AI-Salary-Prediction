// Set this to your deployed Render service URL before the final Netlify deployment.
// Example: https://your-salary-api.onrender.com
const API_BASE_URL = "https://ai-salary-prediction-api.onrender.com";

const form = document.getElementById("prediction-form");
const loader = document.getElementById("loader");
const errorMessage = document.getElementById("error-message");
const predictButton = document.getElementById("predict-button");

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove("d-none");
}

function hideError() {
    errorMessage.textContent = "";
    errorMessage.classList.add("d-none");
}

function fillSelect(id, values, placeholder) {
    const select = document.getElementById(id);
    select.innerHTML = "";

    const first = document.createElement("option");
    first.value = "";
    first.textContent = placeholder;
    first.disabled = true;
    first.selected = true;
    select.appendChild(first);

    values.forEach((value) => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
    });
}

async function loadOptions() {
    if (API_BASE_URL.includes("REPLACE_WITH_YOUR_RENDER_URL")) {
        showError("Backend URL is not configured yet. We will add your Render URL after deployment.");
        ["gender", "education", "job"].forEach((id) => {
            document.getElementById(id).innerHTML = '<option value="">Backend URL required</option>';
        });
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/options`);
        if (!response.ok) throw new Error("Could not load form options from the backend.");
        const options = await response.json();

        fillSelect("gender", options.genders, "Select gender");
        fillSelect("education", options.educations, "Select education level");
        fillSelect("job", options.jobs, "Select job title");
    } catch (error) {
        showError(`${error.message} Please check that the Render backend is running.`);
    }
}

function animateSalary(target) {
    const element = document.getElementById("salary-value");
    const duration = 900;
    const startTime = performance.now();

    function update(now) {
        const progress = Math.min((now - startTime) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = target * eased;
        element.textContent = `₹ ${current.toLocaleString("en-IN", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        })}`;
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

function displayPrediction(result) {
    document.getElementById("empty-state").classList.add("d-none");
    document.getElementById("prediction-results").classList.remove("d-none");

    animateSalary(Number(result.prediction));
    document.getElementById("candidate-score").textContent = `${result.score}%`;
    document.getElementById("hiring-chance").textContent = `${result.hiring}%`;
    document.getElementById("salary-rating").textContent = result.rating;
    document.getElementById("prediction-status").textContent = "✔ Success";
    document.getElementById("experience-category").textContent = result.category;
    document.getElementById("hr-recommendation").textContent = result.recommendation;
    document.getElementById("ai-suggestion").textContent = result.ai_suggestion;

    const progress = document.getElementById("experience-progress");
    progress.style.width = `${result.progress}%`;
    progress.textContent = `${result.progress}%`;
    progress.setAttribute("aria-valuenow", result.progress);

    if (window.confetti) {
        window.confetti({ particleCount: 100, spread: 75, origin: { y: 0.65 } });
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    hideError();

    if (API_BASE_URL.includes("REPLACE_WITH_YOUR_RENDER_URL")) {
        showError("Backend URL is not configured yet. Complete the Render deployment first.");
        return;
    }

    const payload = {
        age: document.getElementById("age").value,
        gender: document.getElementById("gender").value,
        education: document.getElementById("education").value,
        experience: document.getElementById("experience").value,
        job: document.getElementById("job").value
    };

    loader.classList.remove("d-none");
    predictButton.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (!response.ok || result.status !== "success") {
            throw new Error(result.message || "Salary prediction failed.");
        }
        displayPrediction(result);
    } catch (error) {
        showError(error.message || "Could not connect to the prediction server.");
    } finally {
        loader.classList.add("d-none");
        predictButton.disabled = false;
    }
});

// Preserve the original dashboard hover, scroll and logo effects.
window.addEventListener("load", () => {
    document.querySelectorAll(".mini-card,.dashboard-card").forEach((card) => {
        card.addEventListener("mouseenter", () => card.style.transform = "translateY(-8px)");
        card.addEventListener("mouseleave", () => card.style.transform = "translateY(0)");
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll(".glass-card,.mini-card,.dashboard-card,.salary-result,.ai-card")
        .forEach((element) => {
            element.style.opacity = "0";
            element.style.transform = "translateY(24px)";
            element.style.transition = ".8s";
            observer.observe(element);
        });

    const logo = document.querySelector(".logo-circle");
    if (logo) {
        logo.addEventListener("mouseover", () => logo.style.transform = "rotate(360deg) scale(1.1)");
        logo.addEventListener("mouseout", () => logo.style.transform = "rotate(0deg) scale(1)");
    }
});

const rippleStyle = document.createElement("style");
rippleStyle.textContent = `
.btn-primary { position: relative; overflow: hidden; }
@keyframes ripple { to { transform: scale(4); opacity: 0; } }
`;
document.head.appendChild(rippleStyle);

predictButton.addEventListener("click", function (event) {
    const circle = document.createElement("span");
    const diameter = Math.max(this.clientWidth, this.clientHeight);
    const rect = this.getBoundingClientRect();
    circle.style.cssText = `
        width:${diameter}px;height:${diameter}px;position:absolute;
        border-radius:50%;background:rgba(255,255,255,.4);
        left:${event.clientX - rect.left - diameter / 2}px;
        top:${event.clientY - rect.top - diameter / 2}px;
        transform:scale(0);animation:ripple .6s linear;pointer-events:none;
    `;
    this.appendChild(circle);
    setTimeout(() => circle.remove(), 650);
});

loadOptions();
