document.addEventListener("DOMContentLoaded", function() {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    const currentTab = tabs[0];
    document.getElementById('url').value = currentTab.url;
    document.getElementById('title').value = currentTab.title;
  });

  // Keeping the save button functionality as it was:
  document.getElementById('saveBtn').addEventListener('click', function() {
    chrome.runtime.sendMessage({
        url: document.getElementById('url').value,
        title: document.getElementById('title').value
    }, (response) => {
        if (response && response.success) {
            const successElem = document.getElementById('success');
            successElem.style.display = 'flex';
            
            // Set a timeout to hide the checkmark after 2 seconds
            setTimeout(() => {
                successElem.style.display = 'none';
            }, 2000);
        }
    });
  });
});


