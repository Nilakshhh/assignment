// This function will be called when an employee is 
// added into the database by an user, 
// it makes a POST request to /api/employee route

document.getElementById("employeeForm").addEventListener("submit", function(event) {
    event.preventDefault(); 

    const formData = new FormData(event.target);

    const jsonObject = {};
    formData.forEach(function(value, key){
        jsonObject[key] = value;
    });

    fetch('/api/employees', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonObject)
    })
    .then(response => {
        if (response.ok) {
            alert("Employee added successfully!, redirecting...");
            setTimeout(function() {
                window.location.href = '/profile';
            }, 2000); 
        } else {
            alert("Failed to add employee. Please try again.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred. Please try again later.");
    });
});