// Function to fetch employee data from Flask route
function fetchEmployeeData() {
    fetch('/api/employees')
        .then(response => response.json())
        .then(data => populateTable(data))
        .catch(error => console.error('Error fetching employee data:', error));
}

// Function to populate table with employee data
function populateTable(data) {
    var table = document.getElementById("employeeTable");
    for (var i = 0; i < data.length; i++) {
        var row = table.insertRow(-1);
        for (var j = 0; j < data[i].length; j++) {
            var cell = row.insertCell(-1);
            cell.innerHTML = data[i][j];
        }
    }
}

// Call the function to fetch employee data
fetchEmployeeData();