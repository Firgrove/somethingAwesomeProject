export const decrypt = (message, key) => {
    const encrypted_bytes = Buffer.from(encrypted_text, 'base64');
    const iv = encrypted_bytes.slice(0, 16);
    const ciphertext = encrypted_bytes.slice(16);
    const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
    decipher.setAutoPadding(false); // disable automatic padding
    const decrypted_text = decipher.update(ciphertext);
    const unpadded_text = Buffer.concat([decrypted_text, decipher.final()]);
    return unpadded_text.toString('utf8');
}

/**
 * Performs a request that requires a body
 * @param {String} path The url to make the request to
 * @param {Object} body The body content of the fetch request
 * @returns A promise with the response data or an error message
 */
export const apiCallBody = (path, body, method) => {
    return new Promise((resolve, reject) => {
        fetch('https://localhost:6441/' + path, {
            method: method,
            mode: 'cors',
            headers: {
                'Content-type': 'application/json',
                // Always include token if we have one. Returns null if token does not exist
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(body)
        })
            .catch((reason) => {
                throw new Error('Network Error. Please try again later');
            })
            .then((response) => {
                console.log(response);
                return response.json();
            })
            .then((data) => {
                if (data.error) {
                    console.log(data.error);
                    reject(data.error);
                }
                
                resolve(data);

            }).catch((reason) => {
                reject(reason);
            });
    }); 
};


export const apiCallGet = (path, queryString) => {
    return new Promise((resolve, reject) => {
        fetch('https://localhost:6441/' + path + '?' + queryString, {
            method: 'GET',
            headers: {
            'Content-type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
        })
            .catch((reason) => {
                throw new Error('Network Error. Please try again later');
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    reject(data.error);
                } else {
                    resolve(data);
                }
            });
    });
};


// Convert an ArrayBuffer into a string.
// From https://developers.google.com/web/updates/2012/06/How-to-convert-ArrayBuffer-to-and-from-String
function arrayBufToString(buf) {
	return String.fromCharCode.apply(null, new Uint8Array(buf));
}

function pemEncode(label, data) {
	const base64encoded = window.btoa(data);
	const base64encodedWrapped = base64encoded.replace(/(.{64})/g, "$1\n");
	return `-----BEGIN ${label}-----\n${base64encodedWrapped}\n-----END ${label}-----`;
}

async function exportKeyAsString(format, key) {
	const exported = await window.crypto.subtle.exportKey(format, key);
	return arrayBufToString(exported);
}

export async function pemEncodedPrivateKey(keyPair) {
	const exported = await exportKeyAsString("pkcs8", keyPair.privateKey);
	return pemEncode("PRIVATE KEY", exported);
}

export async function pemEncodedPublicKey(keyPair) {
	const exported = await exportKeyAsString("spki", keyPair.publicKey);
	return pemEncode("PUBLIC KEY", exported);
}