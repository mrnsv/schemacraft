const jsonInput = document.getElementById('jsonInput');
const schemaOutput = document.getElementById('schemaOutput');
const convertBtn = document.getElementById('convertBtn');
const darkModeBtn = document.getElementById('darkModeBtn');
const body = document.body;

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
            schemaOutput.textContent = JSON.stringify(schema, null, 2);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

darkModeBtn.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
        darkModeBtn.textContent = '☀️';
    } else {
        darkModeBtn.textContent = '🌙';
    }
});