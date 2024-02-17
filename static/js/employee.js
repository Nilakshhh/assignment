function fetchEmployeeData() {
    fetch('/api/employees')
        .then(response => response.json())
        .then(data => populateTable(data))
        .then(showEmployeeTable())
        .then(hideEmployeeInfoDiv())
        .catch(error => console.error('Error fetching employee data:', error));
}

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

function showEmployeeTable() {
    const employeeDataTable = document.getElementById("employeeTable");
    employeeDataTable.style.display = "block";
}

function hideEmployeeInfoDiv() {
    const employeeInfoDiv = document.getElementById("employeeInfo");
    employeeInfoDiv.style.display = "none";
}

function searchEmployee() {
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