const crypto = require('crypto');

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
        fetch('http://localhost:5005/' + path, {
            method: method,
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
        fetch('http://localhost:5005/' + path + '?' + queryString, {
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