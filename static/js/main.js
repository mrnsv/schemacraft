const jsonInput = document.getElementById('jsonInput');
const schemaOutput = document.getElementById('schemaOutput');
const convertBtn = document.getElementById('convertBtn');
const darkModeBtn = document.getElementById('darkModeBtn');
const body = document.body;
const errorMessage = document.getElementById('errorMessage');
const copyBtn = document.getElementById('copyBtn');

// Ensure copy button is initially hidden
copyBtn.style.display = 'none'; 

convertBtn.addEventListener('click', () => {
    const jsonData = jsonInput.value;
    if (jsonData) {
        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData
        })
        .then(response => response.json())
        .then(schema => {
            errorMessage.textContent = '';  // Clear any previous error message
            schemaOutput.textContent = JSON.stringify(schema, null, 2);
            // Make copy button visible after successful conversion
          copyBtn.style.display = 'inline-block';
        })
        .catch(error => {
            errorMessage.textContent = 'Error: ' + error.message;  // Display error message
            console.error('Error:', error);
            // Hide copy button in case of errors
            copyBtn.style.display = 'none';
        });
    }
});

copyBtn.addEventListener('click', () => {
    const schemaText = schemaOutput.textContent;
    if (!navigator.clipboard) {
      // Clipboard API not supported, fallback to copy text manually
      errorMessage.textContent = 'Clipboard API not supported. Please select and copy manually.';
      return;
    }
    navigator.clipboard.writeText(schemaText)
      .then(() => {
        copyBtn.classList.add('copied'); // Add 'copied' class for animation
        setTimeout(() => {
          copyBtn.classList.remove('copied'); // Remove 'copied' class after animation
        }, 1000); // Adjust animation duration (1 second in this example)
      })
      .catch(error => {
        errorMessage.textContent = 'Error copying to clipboard: ' + error;
      });
  }); 

darkModeBtn.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
        darkModeBtn.textContent = '☀️';
    } else {
        darkModeBtn.textContent = '🌙';
    }
});
