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
        title: document.getElementById('title').value,
        summary: document.getElementById('summaryText').value,
        type: document.getElementById('contentType').value
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

  // Add a click event listener to the summarize button
  document.getElementById('summarizeBtn').addEventListener('click', function() {
      blockUIElements();

      // Call the fetchSummaryForURL function
      fetchSummaryForURL().then(summary => {
          // Populate the textarea with the summary
          document.getElementById('summaryText').value = summary;
          unblockUIElements();

      }).catch(error => {
          document.getElementById('errorMsg').innerText = "Error: " + error;
          document.getElementById('errorMsg').style.display = 'block';

          unblockUIElements();

          // Hide the error message after 2 seconds
          setTimeout(() => {
              document.getElementById('errorMsg').style.display = 'none';
          }, 2000);
      });
  });
});


// New function to fetch the summary
function fetchSummaryForURL() {
  return new Promise((resolve, reject) => {
      const url = document.getElementById('url').value;
    
      // Instead of directly updating the UI, resolve or reject the promise
      fetch(`http://127.0.0.1:8000/summary?url=${encodeURIComponent(url)}`)
      .then(response => {
          if (response.ok) {
              return response.json();
          }
          return response.json().then(errorData => {
              throw new Error(errorData.message);
          });
      })
      .then(data => {
          resolve(data.summary);
      })
      .catch(error => {
          reject(error.message);
      });
  });
}

function blockUIElements() {
  document.getElementById('summaryText').setAttribute('readonly', 'readonly'); 
  document.getElementById('summarizeBtn').disabled = true;
  document.getElementById('saveBtn').disabled = true;
  document.getElementById('spinner').style.display = 'block';
}

function unblockUIElements() {
  document.getElementById('summaryText').removeAttribute('readonly');
  document.getElementById('summarizeBtn').disabled = false;
  document.getElementById('saveBtn').disabled = false;
  document.getElementById('spinner').style.display = 'none';
}




