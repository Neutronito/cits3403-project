let clickedUser = null; //The <li> element that has been clicked last
let activeUser = null; //The active user (the user currently in focus)
let setAdminStatus = null; //The boolean which the new admin status will be of the activeUser

function refreshUserList() {
    //First clear the list
    var xhttp = new XMLHttpRequest
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let list = document.getElementById("userList");
            //First clear the list
            while (list.firstChild) {
                list.removeChild(list.lastChild);
            }
            //Now add all our obtained users to the list 
            const userList = JSON.parse(this.responseText).user_list

            userList.forEach(function(currentValue) {
                listElement = document.createElement("li");
                listElement.innerHTML = currentValue;
                listElement.addEventListener("click", userListItemClick);
                list.appendChild(listElement);
            })

            clickedUser = list.firstChild;
            list.firstChild.click();
            
        }
    };

    xhttp.open("GET", base_path + "/admin/api/user/all", true)
    xhttp.send()
}

function userListItemClick() {
    clickedUser.style.backgroundColor = "WHITE";
    clickedUser.style.color = "BLACK";

    this.style.backgroundColor = "BLACK";
    this.style.color = "WHITE";

    clickedUser = this;
    activeUser = clickedUser.innerHTML;
    
    updateActiveUserInfo();
}

function updateActiveUserInfo() {
    //Update the users name
    document.getElementById("currentUser").innerHTML = activeUser;

    //Update the users password


    //Update the users count
    var xhttpCount = new XMLHttpRequest;
    xhttpCount.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let count = JSON.parse(this.responseText).count;
            document.getElementById("count").innerHTML = count;
        }
    };
    xhttpCount.open("GET", base_path + "/game/api/count?user=" + activeUser, true);
    xhttpCount.send();

    //Update the users admin status
    var xhttpAdmin = new XMLHttpRequest;
    xhttpAdmin.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let isAdmin = JSON.parse(this.responseText).admin;
            if (isAdmin) {
                isAdmin = "Admin";
            } else {
                isAdmin = "Not Admin";
            }
            document.getElementById("adminStatus").innerHTML = isAdmin;

            refreshAdminButton(); 
        }
    };
    xhttpAdmin.open("GET", base_path + "/admin/api/user/is-admin?user=" + activeUser, true);
    xhttpAdmin.send();
}

function modifyUserCount() {
    let integerCount = parseInt(document.getElementById("countForm").value);
    document.getElementById("countForm").value = "";
    
    if (Number.isNaN(integerCount)) {
        alert("Error, you must input a number for the count.")
        return;
    }

    // Confirmation code to avoid accidental modification of a user's count
    let confirmPrompt = window.prompt("This will permanently modify " + activeUser + "'s count. Are you sure you wish to continue? If so, type in their username.","");
    if (confirmPrompt == null) {
        return;
    } else if (confirmPrompt !== activeUser) {
        alert("Confirmation failed. " + activeUser + "'s count was not modified.")
        return;
    }

    let amount = integerCount - parseInt(document.getElementById("count").innerHTML);

    if (amount > 0) {
        var action = "increment";
    } else if (amount < 0) {
        var action = "decrement"
        amount *= -1;
    } else {
        return
    }



    // Set the count to the input count
    var xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            updateActiveUserInfo();
        }
    }

    xhttp.open("POST", base_path + "/game/api/count?user=" + activeUser + "&action=" + action + "&amount=" +amount, true);
    xhttp.send();    

}

function refreshAdminButton() {
    if (document.getElementById("adminStatus").innerHTML === "Admin") {
        document.getElementById("adminButton").innerHTML = "Remove " + activeUser + " admin"
        setAdminStatus = "false";
    } else {
        document.getElementById("adminButton").innerHTML = "Make " + activeUser + " admin"
        setAdminStatus = "true"
    }
}

function changeUserAdmin() {
    // Confirmation code to avoid accidental modification of a user's admin state
    if (setAdminStatus === "true") {
        var promptText = "Warning, this will make " + activeUser + " admin. Are you sure you wish to continue? If so, type in their username." 
    } else {
        var promptText = "Warning, this will remove admin from " + activeUser + ". Are you sure you wish to continue? If so, type in their username"
    }
    let confirmPrompt = window.prompt(promptText,"");
    if (confirmPrompt == null) {
        return;
    } else if (confirmPrompt !== activeUser) {
        alert("Confirmation failed. " + activeUser + "'s admin state was not modified.")
        return;
    }

    var xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 204) {
            updateActiveUserInfo();
        }
    }

    xhttp.open("PUT", base_path + "/admin/api/user/admin?user=" + activeUser + "&adminFlag=" + setAdminStatus);
    xhttp.send();  
}

// Just refreshes the userList which will nicely initalize everything
function bodyOnload() {
    refreshUserList();
}