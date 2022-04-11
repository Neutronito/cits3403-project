let global_count = 0;
let count = 0;

function api_call(myData, getRoute, request_type) {

  return $.ajax({
      url: getRoute + "?" + jQuery.param(myData),
      type: request_type,
      success: function(d) {
          global_count = d["count"];
          zeroCounter();
      }
  })
}

// Refreshes the counter display
function refreshCounter(){
    document.getElementById("clickCount").innerHTML = "You have pressed the button " + (global_count + count) + " times!";
}

// Increments the counter when you push the button on the homepage
function incrementCounter() {
    count += 1;
    refreshCounter();
}
// Decrements the counter when the button is pushed on the homepage, only if the count is above 0
function decrementCounter() {
    count -= 1;
    refreshCounter();
}
// Zeros the count value
function zeroCounter() {
    count = 0;
    refreshCounter();
}

function resetCounter() {
    count = 0;
    api_call(null, '/api/v1/count', 'DELETE');
}

// Submits the count value and then returns it
function submitCounter() {
    let action;
    if (count >= 0) {
        action = 'increment';
    } else {
        action = 'decrement';
    }
    const myData = {
        'action': action,
        'amount': Math.abs(count),
    };
    api_call(myData, '/api/v1/count', 'POST');
}

function fetchCount() {
    api_call(null, '/api/v1/count', 'GET');
}
