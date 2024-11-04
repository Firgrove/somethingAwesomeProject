import { 
    apiCallGet, 
    apiCallBody, 
    decrypt,
    spkiToPEM
 } from './helpers.js';

console.log('frontend starting up');

const renderMessages = () => {
    document.getElementById('login').style.display = 'none';
    document.getElementById('messages').style.display = 'flex';
    document.getElementById('register').style.display = 'none';
    document.getElementById('logout-button').style.display = 'block';
}

async function handleLogin(form) {
    console.log('logging in');
    if (form['username'].length === 0) {alert('please enter a username')}
    if (form['password'].length === 0) {alert('please enter a passsword')}

    let pub_key = null;
    if (!localStorage.getItem('deviceID')) {
        // Generate public private key pair
        try {
            let keyPair = await window.crypto.subtle.generateKey(
                {
                name: "RSA-OAEP",
                modulusLength: 4096,
                publicExponent: new Uint8Array([1, 0, 1]),
                hash: "SHA-256",
                },
                true,
                ["encrypt", "decrypt"],
            );
            
            // Export key to send to python
            console.log(`keypair: ${keyPair.publicKey}`);
            const pemPubKey = spkiToPEM(window.crypto.subtle.exportKey("spki",keyPair.publicKey));
            console.log(pemPubKey)
        } catch (error) {
            alert("login failed, username or password are likely wrong.");
            return;
        }
    } 

    localStorage.setItem('username', form['username'])

    const body = {
        'username': form['username'].value,
        'password': form['password'].value,
        'deviceID': localStorage.getItem('deviceID'),
        'pub_key': pub_key
    }

    console.log(body);
    console.log(JSON.stringify(body));

    apiCallBody('login', body, 'POST').then((data) => {
        console.log('server succeeded');
        console.log(data);
        localStorage.setItem('deviceID', data.deviceID);
        localStorage.setItem('token', data.token);
        renderMessages();
    }).catch((error) => {
        alert(`login failed with error: ${error}`);
    });
}

async function handleRegister(form) {
    console.log('registering account');

    if (form['username'].length === 0) {alert('please enter a username')}
    if (form['password'].length === 0) {alert('please enter a passsword')}

    localStorage.setItem('username', form['username'])

    // Generate public private key pair
    try {
        let keyPair = await window.crypto.subtle.generateKey(
            {
              name: "RSA-OAEP",
              modulusLength: 4096,
              publicExponent: new Uint8Array([1, 0, 1]),
              hash: "SHA-256",
            },
            true,
            ["encrypt", "decrypt"],
        );
        
        const pemPubKey = spkiToPEM(window.crypto.subtle.exportKey("spki",keyPair.publicKey));
        console.log(pemPubKey)
    } catch (error) {
        alert(error);
        return;
    }
      
    const body = {
        'username': form['username'].value,
        'password': form['password'].value,
        'pub_key': null
    }

    localStorage.setItem('deviceID', 0)

    apiCallBody('register', body, 'POST').then((data) => {
        console.log('server succeeded');
        console.log(data);
        localStorage.setItem('token', data.token);
        renderMessages();
    }).catch(() => {
        alert('Failed to create account. Please check your details and try again'); 
    });
}

const logout = () => {
    if (!localStorage.getItem('token')) {alert('already logged out')}

    const body = {'token': localStorage.getItem('token')}
    localStorage.removeItem('token');
    renderLogin();
    apiCallBody('logout', body, 'POST');
}

const handleLoginSubmit = (event) => {
    event.preventDefault();
    const form = event.target;

    handleLogin(form);
}

const handleRegisterForm = (event) => {
    event.preventDefault();
    const form = event.target;

    handleRegister(form);
}

const renderRegister = (event) => {
    document.getElementById('login').style.display = 'none';
    document.getElementById('messages').style.display = 'none';
    document.getElementById('register').style.display = 'flex';
    document.getElementById('logout-button').style.display = 'none';
}

const renderLogin = (event) => {
    document.getElementById('login').style.display = 'flex';
    document.getElementById('messages').style.display = 'none';
    document.getElementById('register').style.display = 'none';
    document.getElementById('logout-button').style.display = 'none';
}



console.log('adding event listeners')

document.getElementById('logout-button').addEventListener('click', logout);
document.getElementById('login-form').addEventListener('submit', handleLoginSubmit);
document.getElementById('register-form').addEventListener('submit', handleRegisterForm);
document.getElementById('goto-page-register').addEventListener('click', renderRegister);
document.getElementById('goto-page-login').addEventListener('click', renderLogin);