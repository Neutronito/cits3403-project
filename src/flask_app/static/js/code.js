let count = 0;
let username = null;

function api_call(myData, getRoute, request_type) {
    
    try{
      $.ajax({
        url: getRoute + username + '?' + jQuery.param(myData),
        type: request_type,
      })
    }
    catch (ex){
      alert(ex);
    }
  }

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
    var getRoute = '/api/v1/count/';
    if(count >= 0){
        var action = 'increment';        
    }
    else{
        var action = 'decrement';
    }
    var myData = {
        'action': action,
        'amount': count
    }; 
    api_call(myData, getRoute,'PUT');
}

// Called when the user hits submit on the login page
function submitClicked() {
    username = getInputString('unameInput');
    let pwr = getInputString('pwrInput');
    getRoute = "/api/v1/user/";
    api_call(null, getRoute, 'POST');
    var a = api_call(null, getRoute,  'GET');
    count = a["count"];
    document.getElementById("displayLogin").innerHTML = "Your username is " + username + " and your password is " + pwr + "!";
}

// Returns the contens of the input which is identified through the given id
function getInputString(inputID) {
    return document.getElementById(inputID).value;
}