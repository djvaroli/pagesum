chrome.runtime.onMessage.addListener(function(data, sender, sendResponse) {
    fetch('http://127.0.0.1:8000/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.status === 200) {
            sendResponse({ success: true });
        } else {
            sendResponse({ success: false });
        }
        return response.json();
    }).then(data => {
        console.log(data.message);
    }).catch(error => {
        console.error('Error:', error);
    });
    return true;  // indicates the response is sent asynchronously
});
