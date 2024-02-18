// This function will be called when an employee is 
// added into the database by an user, 
// it makes a POST request to /api/employee route

// emailValidator.js
class EmailValidator {
    constructor() {
      this.emailRegex = /^[a-zA-Z0-9._-]+@company\.com$/;
    }
  
    isValidEmail(email) {
      return this.emailRegex.test(email);
    }
  }

function adduser(event){
    event.preventDefault();
    const formData = new FormData(event.target);

    const jsonObject = {};
    formData.forEach(function(value, key){
        jsonObject[key] = value;
    });

    const validator = new EmailValidator();
    if(validator.isValidEmail(jsonObject['email'])){
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
            } else if(response.status == 409){
                alert("Email already exists");
            } else{
                console.log(response.status);
                alert("Failed to add employee. Please try again.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred. Please try again later.");
        });
    } else {
        alert("Please enter a valid email-address");
    }

}