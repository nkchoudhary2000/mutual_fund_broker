document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("You must be logged in to access the dashboard.");
        window.location.href = "/";
        return;
    }

    try {
        const response = await fetch("/portfolio", {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to fetch portfolio.");
        }

        displayPortfolio(data);
    } catch (error) {
        document.getElementById("portfolio").innerHTML = `<p class="error">${error.message}</p>`;
    }
});

function displayPortfolio(investments) {
    if (!investments.length) {
        document.getElementById("portfolio").innerHTML = "<p>No investments found.</p>";
        return;
    }

    let html = `
        <table>
            <thead>
                <tr>
                    <th>Scheme Name</th>
                    <th>Fund Family</th>
                    <th>Units</th>
                    <th>NAV</th>
                    <th>Invested On</th>
                </tr>
            </thead>
            <tbody>
    `;

    investments.forEach(inv => {
        html += `
            <tr>
                <td>${inv.scheme_name}</td>
                <td>${inv.fund_family}</td>
                <td>${inv.units}</td>
                <td>${inv.nav}</td>
                <td>${new Date(inv.invested_on).toLocaleDateString()}</td>
            </tr>
        `;
    });

    html += `</tbody></table>`;
    document.getElementById("portfolio").innerHTML = html;
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
}
