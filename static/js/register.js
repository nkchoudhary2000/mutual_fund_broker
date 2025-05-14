async function handleRegister(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();

    if (response.ok) {
        alert("Registration successful!");
        window.location.href = "/";
    } else {
        document.getElementById("error").innerText = result.detail;
    }
}
