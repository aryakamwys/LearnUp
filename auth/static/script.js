function showModal(type) {
    document.getElementById('modal-bg').classList.remove('hidden');
    if (type === 'login') {
        document.getElementById('loginModal').classList.remove('hidden');
        document.getElementById('registerModal').classList.add('hidden');
    } else {
        document.getElementById('registerModal').classList.remove('hidden');
        document.getElementById('loginModal').classList.add('hidden');
    }
}
function closeModal() {
    document.getElementById('modal-bg').classList.add('hidden');
    document.getElementById('loginModal').classList.add('hidden');
    document.getElementById('registerModal').classList.add('hidden');
}
async function handleRegister(event) {
    event.preventDefault();
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const query = `
        mutation {
            registerUser(username: "${username}", email: "${email}", password: "${password}") {
                ok
                message
                user { id username }
            }
        }
    `;
    try {
        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        const result = await response.json();
        if (result.data.registerUser.ok) {
            alert('Registration successful!');
            showModal('login');
        } else {
            alert(result.data.registerUser.message);
        }
    } catch (error) {
        alert('Error during registration: ' + error.message);
    }
}
async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const query = `
        mutation {
            loginUser(username: "${username}", password: "${password}") {
                ok
                message
                user { id username }
            }
        }
    `;
    try {
        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        const result = await response.json();
        if (result.data.loginUser.ok) {
            window.location.href = 'http://localhost:5002/';
        } else {
            alert(result.data.loginUser.message);
        }
    } catch (error) {
        alert('Error during login: ' + error.message);
    }
}
