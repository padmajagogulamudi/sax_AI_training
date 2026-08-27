let editId = null;

let emps = [
    {
        id: 1,
        ename: "Ram",
        salary: 5000000
    },
    {
        id: 3,
        ename: "Sony",
        salary: 100000
    }
];


// ================= READ =================

function displayEmployees() {

    let table = document.getElementById("employeeTable");

    table.innerHTML = "";

    emps.forEach(function(employee) {

        let row = `
            <tr>
                <td>${employee.id}</td>
                <td>${employee.ename}</td>
                <td>${employee.salary}</td>

                <td>

                    <button onclick="editEmployee(${employee.id})">
                        Edit
                    </button>

                    <button onclick="deleteEmployee(${employee.id})">
                        Delete
                    </button>

                </td>
            </tr>
        `;

        table.innerHTML += row;
    });
}


// ================= CREATE / UPDATE =================

document.getElementById("employeeForm").addEventListener("submit", function(event) {

    event.preventDefault();

    let id = Number(document.getElementById("id").value);
    let name = document.getElementById("ename").value;
    let salary = Number(document.getElementById("salary").value);

    let employee = {
        id: id,
        ename: name,
        salary: salary
    };


    // CREATE

    if (editId === null) {

        emps.push(employee);

    }


    // UPDATE

    else {

        let employeeIndex = emps.findIndex(function(employee) {

            return employee.id === editId;

        });

        emps[employeeIndex] = employee;

        editId = null;
    }


    displayEmployees();

    document.getElementById("employeeForm").reset();
});


// ================= DELETE =================

function deleteEmployee(id) {

    emps = emps.filter(function(employee) {

        return employee.id !== id;

    });

    displayEmployees();
}


// ================= EDIT =================

function editEmployee(id) {

    let employee = emps.find(function(employee) {

        return employee.id === id;

    });

    editId = id;

    document.getElementById("id").value = employee.id;

    document.getElementById("ename").value = employee.ename;

    document.getElementById("salary").value = employee.salary;
}


// Display initial employees

displayEmployees();