// This file will handle api calls made by employee or manager
// for various operations

function fetchEmployeeData() {
    //This function makes a simple GET request to obtain data of all employees

    fetch('/api/employees')
        .then(response => response.json())
        .then(data => populateTable(data))
        .then(showEmployeeTable())
        .then(hideEmployeeInfoDiv())
        .catch(error => console.error('Error fetching employee data:', error));
}

function searchEmployee() {
    // Function to search for an employee by id, once information is retrieved, 
    // it is displayed with helper functions else, error is shown

    const employeeId = document.getElementById('employeeId').value;

    fetch(`/api/employees/${employeeId}`, {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Employee not found');
        }
        return response.json();
    })
    .then(data => {
        displayEmployee(data);
    })
    .catch(error => {
        alert(error.message);
    });
}

function submitUpdate() {
    // This function makes a PUT request to the server to update 
    // an employee data based on information given by the user

    const email = document.getElementById('email').value;
    const role = document.getElementById('role').value;
    const password = document.getElementById('password').value;
    const empId = parseInt(document.getElementById('employeeId').value);

    hideEmployeeInfoDiv();

    const newData = {
    email: email,
    role: role,
    password: password
    };

    fetch(`/api/employees/${empId}`, {
    method: 'PUT',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(newData)
    })
    .then(response => {
    if (!response.ok) {
        throw new Error('Failed to update employee.');
    }
    return response.json();
    })
    .then(data => {
    if (data.success) {
        alert("Employee updated successfully.");
        editEmployeeForm.style.display = 'none';
    } else {
        alert("Failed to update employee: " + data.error);
    }
    })
    .catch(error => {
    console.error('Error:', error);
    alert("Failed to update employee: " + error.message);
    });
}

function logout() {
    //This function will remove the token from saved cookie and will logout the current user

    fetch('/logout', {
        method: 'POST',
        credentials: 'same-origin'
    })
    .then(response => {
        if (response.ok) {
            document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            window.location.href = '/';
        } else {
            console.error('Failed to logout:', response.statusText);
            alert('Failed to logout. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}

// Helper functions to make changes in UI

function populateTable(data) {
    var table = document.getElementById("employeeTable");
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }

    for (var i = 0; i < data.length; i++) {
        var row = table.insertRow(-1);
        for (var j = 0; j < data[i].length; j++) {
            var cell = row.insertCell(-1);
            cell.innerHTML = data[i][j];
        }
    }
}

function displayEmployee(employee) {
    const employeeInfoDiv = document.getElementById('employeeInfo');
    employeeInfoDiv.style.display = "block";
    document.getElementById("employeeTable").style.display = "none";

    employeeInfoDiv.innerHTML = `
        <h2>Employee Details</h2>
        <p>ID: ${employee[0][0]}</p>
        <p>Email: ${employee[0][1]}</p>
        <p>Role: ${employee[0][2]}</p>
        <p>Created at: ${employee[0][3]}</p>
    `;
}

function showEmployeeTable() {
    const employeeDataTable = document.getElementById("employeeTable");
    employeeDataTable.style.display = "block";
}

function hideEmployeeInfoDiv() {
    const employeeInfoDiv = document.getElementById("employeeInfo");
    employeeInfoDiv.style.display = "none";
}

function hideEditForm() {
    document.getElementById('editEmployeeForm').style.display = 'none';
}


function hideEditButtons() {
    document.getElementById('editButtons').style.display = 'none';
}

function showEditForm() {
    hideEditButtons();
    const editEmployeeForm = document.getElementById('editEmployeeForm');
    editEmployeeForm.innerHTML = `
        <h2>Edit Employee</h2>
        <label for="email">Email:</label>
        <input type="text" id="email">
        <label for="role">Role:</label>
        <input type="text" id="role">
        <label for="password">Password:</label>
        <input type="text" id="password">
        <button onclick="submitUpdate()">Save Changes</button>
    `;
    editEmployeeForm.style.display = 'block';
}