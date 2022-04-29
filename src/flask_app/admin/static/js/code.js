function initTable() {
    var xhttp = new XMLHttpRequest
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let adminTable = document.getElementById("adminTable");

            //Now add all our obtained users to the table 
            const userList = JSON.parse(this.responseText).user_list
            let todayUTC = new Date((new Date()).toUTCString())
            userList.forEach((element) => {
                //Create a new row
                let newRow = document.createElement("tr");
                newRow.setAttribute('cits3403-user', element)
                //Add the name colummn ~~~~~~~~~~~~~~~~~~
                let nameColumn = document.createElement("td");
                nameColumn.innerHTML = element;
                newRow.appendChild(nameColumn);

                //Add the date column ~~~~~~~~~~~~~~~~~~
                let dateColumn = document.createElement("td");
                let datePicker = document.createElement("input")
                datePicker.setAttribute('cits3403-user', element)
                datePicker.setAttribute('type', 'date')
                datePicker.valueAsDate = todayUTC;
                datePicker.setAttribute('max', todayUTC.toISOString().slice(0, -14));
                datePicker.setAttribute('required', 'true');
                dateColumn.appendChild(datePicker);
                newRow.appendChild(dateColumn);

                //Add the count ~~~~~~~~~~~~~~~~~~
                let countInput = document.createElement("input");
                let countDiv = document.createElement("div");
                let countCell  = document.createElement("td");
                countInput.type = "number";
                countInput.inputMode = "numeric";
                countInput.setAttribute("cits3403-user", element)
                countInput.addEventListener("change", countSubmit)
                setCountInput("GET","/game/api/count?user=" + element, true, countInput);
                countDiv.appendChild(countInput);

                countCell.appendChild(countDiv);
                newRow.appendChild(countCell);
                DateChange(element, countInput, todayUTC.toISOString().slice(0, -5))
                datePicker.addEventListener('change', (event)=>{
                    DateChange(element, countInput ,event.target.valueAsDate.toISOString().slice(0, -5))
                });

                //Role section ~~~~~~~~~~~~~~~~~~
                let roleCell = document.createElement("td")
                let roleSelect = document.createElement("select");
                roleSelect.name = "role";

                let admin = document.createElement("option");
                admin.value = "Admin";
                admin.innerHTML = "Admin";
                roleSelect.appendChild(admin);

                let user = document.createElement("option");
                user.value = "User";
                user.innerHTML = "User";
                roleSelect.appendChild(user);
                roleSelect.setAttribute("cits3403-user", element)
                setRoleStatus(roleSelect, element);
                roleSelect.addEventListener("change", roleChanged);

                roleCell.appendChild(roleSelect);

                newRow.appendChild(roleCell);

                //Add the delete user button
                let deleteCell = document.createElement("td");

                let deleteButton = document.createElement("button");
                deleteButton.innerHTML = "Delete";
                deleteButton.setAttribute("cits3403-user", element)
                deleteButton.addEventListener("click", deletePressed);
                
                deleteCell.appendChild(deleteButton);

                newRow.appendChild(deleteCell);

                //Add the new user row to the table
                adminTable.appendChild(newRow);
            });    
        }
    };

    xhttp.open("GET", "/admin/api/user/all", true)
    xhttp.send()

}

function DateChange(user, countCell, date) {
    countCell.setAttribute('cits3403-date', date);
    setCountInput("GET", `/game/api/count?user=${user}&date=${date}`, true, countCell)
}

function countSubmit() {
    let countCell = this;
    let user = countCell.getAttribute('cits3403-user');
    let integerCount = parseInt(countCell.value);
    let date = countCell.getAttribute('cits3403-date');

    let amount = integerCount - countCell.placeholder;

    if (amount > 0) {
        var action = "increment";
    } else if (amount < 0) {
        var action = "decrement";
        amount *= -1;
    } else {
        return
    }

    setCountInput("POST", `/game/api/count?user=${user}&action=${action}&amount=${amount}&date=${date}`, true, countCell)
}

function setCountInput(type, path, async, countCell) {
    var xhttp = new XMLHttpRequest
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let count = JSON.parse(this.responseText).count;
            countCell.value = count;
            countCell.placeholder = count; //The place holder will always hold the true count
        }
    };
    xhttp.open(type, path, async);
    xhttp.send();
}

function setRoleStatus(roleSelect, user) {
    var xhttpAdmin = new XMLHttpRequest;
    xhttpAdmin.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let isAdmin = JSON.parse(this.responseText).admin;
            if (isAdmin) {
                roleSelect.value = "Admin";
            } else {
                roleSelect.value = "User";
            }
        }
    };
    xhttpAdmin.open("GET", "/admin/api/user/is-admin?user=" + user, true);
    xhttpAdmin.send();

}

function roleChanged() {
    setUsersRole(this, this.getAttribute('cits3403-user'), this.value);
}
function setUsersRole(roleSelect, user, value) {
    
    let setAdminStatus = (value === "Admin");
    if (setAdminStatus) {
        var promptText = "Warning, this will make " + user + " admin. Are you sure you wish to continue? If so, type in their username." 
    } else {
        var promptText = "Warning, this will remove admin from " + user + ". Are you sure you wish to continue? If so, type in their username"
    }
    let confirmPrompt = window.prompt(promptText,"");
    if (confirmPrompt == null) {
        setRoleStatus(roleSelect, user);
        return;
    } else if (confirmPrompt !== user) {
        alert("Confirmation failed. " + user + "'s admin state was not modified.")
        setRoleStatus(roleSelect, user);
        return;
    }

    var xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 204) {
            setRoleStatus(roleSelect, user);
        }
    }
    xhttp.open("PUT", "/admin/api/user/admin?user=" + user + "&adminFlag=" + setAdminStatus);
    xhttp.send(); 

}

function deletePressed() {
    let user = this.getAttribute('cits3403-user')
    deleteUser(user, document.querySelector(`tr[cits3403-user='${user}']`));
}

function deleteUser(user, currentRow) {
    
    // Confirmation code to avoid accidental modification of a user's count
    let confirmPrompt = window.prompt("This will permanently delete " + user + ". Are you sure you wish to continue? If so, type in their username.","");
    if (confirmPrompt == null) {
        return;
    } else if (confirmPrompt !== user) {
        alert("Confirmation failed. " + user + "'s count was not modified.")
        return;
    }

    // Set the count to the input count
    var xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            //Delete the column from the table
            currentRow.parentElement.removeChild(currentRow);
        }
    }

    xhttp.open("DELETE", "/auth/api/user/" + user, true);
    xhttp.send();   
}