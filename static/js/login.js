async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();

    if (response.ok) {
        localStorage.setItem("token", result.access_token);
        window.location.href = "/dashboard";
    } else {
        document.getElementById("error").innerText = result.detail;
    }
}
