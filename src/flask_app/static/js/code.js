let count = 0;

// Refreshes the counter display
function refreshCounter(){
    document.getElementById("clickCount").innerHTML = "You have pressed the button " + count + " times!";
}

// Increments the counter when you push the button on the homepage
function incrementCounter() {
    count += 1;
    refreshCounter();
}
// Decrements the counter when the button is pushed on the homepage, only if the count is above 0
function decrementCounter() {
    if (count > 0) {
        count -= 1;
        refreshCounter();
    }
}

// Zeros the count value
function zeroCounter() {
    count = 0;
    refreshCounter();
}

// Submits the count value and then returns it
function submitCounter() {
    alert("Your count of " + count + " has been submitted!")
    zeroCounter();
}

// Called when the user hits submit on the login page
function submitClicked() {
    let uname = getInputString('unameInput');
    let pwr = getInputString('pwrInput');
    document.getElementById("displayLogin").innerHTML = "Your username is " + uname + " and your password is " + pwr + "!";
}

// Returns the contens of the input which is identified through the given id
function getInputString(inputID) {
    return document.getElementById(inputID).value;
}