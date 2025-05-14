document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Login required");
        window.location.href = "/";
        return;
    }

    try {
        console.log("Niraj");
        const response = await fetch("/funds/families", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const data = await response.json();
            if (response.status === 429) {
                document.getElementById("schemes").innerHTML = `<p class="error">Rate limit exceeded: ${data.detail}</p>`;
                return;
            }
            throw new Error(data.detail || "Failed to load fund families.");
        }

        const fundFamilies = await response.json();
        console.log(fundFamilies);
        const dropdown = document.getElementById("fund-family");

        fundFamilies.forEach(fund => {
            const option = document.createElement("option");
            option.value = fund;
            option.textContent = fund;
            dropdown.appendChild(option);
        });

    } catch (error) {
        console.error("Error loading fund families:", error);
        document.getElementById("schemes").innerHTML = `<p class="error">Error loading fund families.</p>`;
    }
});

async function fetchSchemes() {
    const token = localStorage.getItem("token");
    const family = document.getElementById("fund-family").value;

    if (!family) return;

    try {
        const response = await fetch(`/funds/schemes?fund_family=${encodeURIComponent(family)}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        const container = document.getElementById("schemes");

        if (!response.ok) {
            const data = await response.json();
            if (response.status === 429) {
                container.innerHTML = `<p class="error">Rate limit exceeded: ${data.detail}</p>`;
                return;
            }
            throw new Error(data.detail || "Failed to load schemes.");
        }

        const schemes = await response.json();
        container.innerHTML = `<h3>${family} - Open Ended Schemes</h3>`;

        if (!schemes.length) {
            container.innerHTML += "<p>No schemes found.</p>";
            return;
        }

        const list = document.createElement("ul");
        schemes.forEach(scheme => {
            const li = document.createElement("li");
            li.textContent = scheme.scheme_name;
            list.appendChild(li);
        });

        container.appendChild(list);

    } catch (error) {
        console.error("Error fetching schemes:", error);
        document.getElementById("schemes").innerHTML = `<p class="error">Error loading schemes.</p>`;
    }
}

function goBack() {
    window.location.href = "/dashboard";
}
