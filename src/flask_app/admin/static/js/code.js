//Deal with the tabs here
function openTab(inEvent, tabID) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabID).style.display = "block";
    inEvent.currentTarget.className += " active";
}

function initAdminTable() {
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
                newRow.setAttribute('data-cits3403-user', element)
                //Add the name colummn ~~~~~~~~~~~~~~~~~~
                let nameColumn = document.createElement("td");
                nameColumn.innerHTML = element;
                newRow.appendChild(nameColumn);

                //Add the date column ~~~~~~~~~~~~~~~~~~
                let dateColumn = document.createElement("td");
                let datePicker = document.createElement("input")
                datePicker.setAttribute('data-cits3403-user', element)
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
                countInput.setAttribute("data-cits3403-user", element)
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
                roleSelect.setAttribute("data-cits3403-user", element)
                setRoleStatus(roleSelect, element);
                roleSelect.addEventListener("change", roleChanged);

                roleCell.appendChild(roleSelect);

                newRow.appendChild(roleCell);

                //Add the delete user button
                let deleteCell = document.createElement("td");

                let deleteButton = document.createElement("button");
                deleteButton.innerHTML = "Delete";
                deleteButton.setAttribute("data-cits3403-user", element)
                deleteButton.addEventListener("click", deletePressed);
                // Style button
                deleteButton.classList.add("tableButton");
                deleteButton.classList.add("btn-primary");

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
    let user = countCell.getAttribute('data-cits3403-user');
    let integerCount = parseInt(countCell.value);
    let date = countCell.getAttribute('cits3403-date');

    let amount = integerCount - countCell.placeholder;

    if(integerCount <= 100){
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
    setUsersRole(this, this.getAttribute('data-cits3403-user'), this.value);
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
    let user = this.getAttribute('data-cits3403-user')
    deleteUser(user, document.querySelector(`tr[data-cits3403-user='${user}']`));
}

function deleteUser(user, currentRow) {
    
    // Confirmation code to avoid accidental modification of a user's count
    let confirmPrompt = window.prompt("This will permanently delete " + user + ". Are you sure you wish to continue? If so, type in their username.");
    if (confirmPrompt == null) {
        return;
    } else if (confirmPrompt !== user) {
        alert("Confirmation failed. " + user + " was not deleted.");
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

//Deal with the map table
function initMapTable() {
    var xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        
            const mapList = JSON.parse(this.responseText);
            
            //Loop through all the maps that are in the db
            // A note to take is that maps are ID from the date they are assigned to
            mapList.forEach((element) => {
                // Create and append new row
                let newRow = document.createElement("tr");
                newRow.setAttribute("map-ID", element.date);
                document.getElementById("mapTable").appendChild(newRow);

                // Add the date column
                let dateColumn = document.createElement("td");
                dateColumn.innerHTML = element.date;
                newRow.appendChild(dateColumn);

                // Add the author column
                let authorColumn = document.createElement("td");
                authorColumn.innerHTML = element.username;
                authorColumn.setAttribute("map-ID", element.date);
                newRow.appendChild(authorColumn)

                // Add the HTML column
                let htmlColumn = document.createElement("td");
                
                //Add the HTML button
                let htmlButton = document.createElement("button");
                htmlButton.innerHTML = "Click for HTML";
                htmlButton.setAttribute("map-ID", element.date);
                htmlButton.addEventListener("click", htmlPressed);

                // Style button
                htmlButton.classList.add("tableButton");
                htmlButton.classList.add("btn-primary");
                
                htmlColumn.appendChild(htmlButton);

                newRow.appendChild(htmlColumn);

                // Add the image column
                let imgColumn = document.createElement("td");
                
                let imgButton = document.createElement("button");
                imgButton.innerHTML = "Click for Image";
                imgButton.setAttribute("map-ID", element.date);
                imgButton.setAttribute("map-width", element.width);
                imgButton.setAttribute("map-height", element.height);
                imgButton.addEventListener("click", imgPressed);

                // Style button
                imgButton.classList.add("tableButton");
                imgButton.classList.add("btn-primary");
                
                imgColumn.appendChild(imgButton);

                newRow.appendChild(imgColumn);

                //Add the delete button
                let delColumn = document.createElement("td");
                
                let delButton = document.createElement("button");
                delButton.innerHTML = "Delete Map";
                delButton.setAttribute("map-ID", element.date);
                delButton.addEventListener("click", delPressed);

                // Style button
                delButton.classList.add("tableButton");
                delButton.classList.add("btn-primary");
                
                delColumn.appendChild(delButton);

                newRow.appendChild(delColumn);

            });
        }
    }
    xhttp.open("GET", "/game/api/map/all", true)
    xhttp.send()
}

function htmlPressed() {
    let mapID = this.getAttribute("map-ID");
    var xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let html = JSON.parse(this.responseText).html
            let newWindow = window.open();
            newWindow.document.write(`<title>HTML Code Preview</title> \n <textarea readonly style="width:100%;height:100%">${html}</textarea>`);
        }
    };

    xhttp.open("GET", "/game/api/map?date=" + mapID, true)
    xhttp.send()
}

function imgPressed() {
    let mapID = this.getAttribute("map-ID");
    let height = this.getAttribute("map-height");
    let width = this.getAttribute("map-width");

    //Get the preview
    var xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let newWindow = window.open();
            let encodedImg = JSON.parse(this.responseText).data;
            newWindow.document.write(`<title>Image Preview</title> \n <img src="data:image/png;base64,${encodedImg}" />`);
        }
    };
    xhttp.open("GET", `/game/api/preview?date=${mapID}&width=${width}&height=${height}`, true);
    xhttp.send();
}

function delPressed() {
    let mapID = this.getAttribute("map-ID");
    let button = this;

    // Confirmation code to avoid accidental modification of a user's count
    let confirmPrompt = window.prompt("This will permanently delete the " + mapID + " map. Are you sure you wish to continue? If so, type in the map's date.");
    if (confirmPrompt == null) {
        return;
    } else if (confirmPrompt !== mapID) {
        alert("Confirmation failed. Map " + mapID + "was not deleted.");
        return;
    }

    var xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            button.parentElement.parentElement.parentElement.removeChild(button.parentElement.parentElement)
        }
    };

    xhttp.open("DELETE", "/game/api/map?date=" + mapID, true)
    xhttp.send();
}

function initAddMap() {
    let todayUTC = new Date((new Date()).toUTCString());
    let datePicker = document.getElementById("date");

    datePicker.setAttribute('min', todayUTC.toISOString().slice(0, -14))
    datePicker.valueAsDate = todayUTC;

    let width = document.getElementById("width");
    let height = document.getElementById("height");

    width.value = 300;
    height.value = 300;
}

function previewNewMap() {
    let map = document.getElementById("map").value;
    let height = document.getElementById("height").value;
    let width = document.getElementById("width").value;

    //Get the preview
    var xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let newWindow = window.open();
            let encodedImg = JSON.parse(this.responseText).data;
            newWindow.document.write(`<img src="data:image/png;base64,${encodedImg}" />`);
        }
    };
    xhttp.open("POST", `/game/api/preview?&width=${width}&height=${height}`, true)
    xhttp.send(map);
}
