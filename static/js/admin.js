let currentEmployeeId;

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
                showEditButtons();
                currentEmployeeId = data.id;
            })
            .catch(error => {
                alert(error.message);
                clearEmployeeInfo();
                hideEditButtons();
                hideEditForm();
            });
        }

        function displayEmployee(employee) {
            const employeeInfoDiv = document.getElementById('employeeInfo');
            employeeInfoDiv.innerHTML = `
                <h2>Employee Details</h2>
                <p>ID: ${employee[0][0]}</p>
                <p>Email: ${employee[0][1]}</p>
                <p>Role: ${employee[0][2]}</p>
                <p>Created at: ${employee[0][3]}</p>
            `;
        }

        function clearEmployeeInfo() {
            document.getElementById('employeeInfo').innerHTML = '';
        }

        function showEditButtons() {
            document.getElementById('editButtons').style.display = 'block';
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

        function hideEditForm() {
            document.getElementById('editEmployeeForm').style.display = 'none';
        }

        function submitUpdate() {
    const email = document.getElementById('email').value;
    const role = document.getElementById('role').value;
    const password = document.getElementById('password').value;
    const empId = parseInt(document.getElementById('employeeId').value);

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
            // Optionally update the UI after successful update
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


        function deleteEmployee() {
            var confirmDelete = confirm("Are you sure you want to delete this employee?");
            const empId = parseInt(document.getElementById('employeeId').value);
            if (confirmDelete) {
                fetch(`/api/employees/${empId}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        alert(data.message);
                        // Optionally update the UI after deletion
                        clearEmployeeInfo();
                        hideEditButtons();
                        hideEditForm();
                    } else {
                        alert("Failed to delete employee.");
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        }