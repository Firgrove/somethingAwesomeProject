import { 
    apiCallGet, 
    apiCallBody, 
    decrypt
 } from './helpers.js';

console.log('frontend starting up');

const handleLogin = (form) => {
    console.log('logging in');
    if (form['username'].length === 0) {alert('please enter a username')}
    if (form['password'].length === 0) {alert('please enter a passsword')}

    pub_key = null;
    if (localStorage.getItem('deviceID')) {
        // TODO: Generate public private key pair
    } 

    body = {
        'username': form['username'].value,
        'password': form['password'].value,
        'deviceID': localStorage.getItem('deviceID')*1,
        'pub_key': pub_key
    }

    apiCallBody('/login', body, 'POST').then((data) => {
        console.log(data);
        localStorage.setItem('deviceID', data.deviceID);
        localStorage.setItem('token', data.token);
    }).catch((error) => {
        alert(`login failed with error: ${error}`);
    });
}

const handleRegister = (form) => {
    console.log('registering account');

    if (form['username'].length === 0) {alert('please enter a username')}
    if (form['password'].length === 0) {alert('please enter a passsword')}

    // TODO: Generate public private key pair

    body = {
        'username': form['username'].value,
        'password': form['password'].value,
        'pub_key': null
    }

    localStorage.setItem('deviceID', 0)

    apiCallBody('/register', body, 'POST').then((data) => {
        console.log(data);
        localStorage.setItem('token', data.token);
    });
}

const logout = () => {
    if (!localStorage.getItem('token')) {alert('already logged out')}

    body = {'token': localStorage.getItem('token')}
    localStorage.removeItem('token');
    apiCallBody('logout', body, 'POST');
}

// TODO: Decryption of messages
// The library I have used so far is symmetric i think. I'll need to fix this