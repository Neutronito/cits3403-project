
var height;
var width;
var date;

function init() {
    var xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
                if (this.status == 200) {
                let obj = JSON.parse(this.responseText);
                height = obj.height;
                width = obj.width;
                date = obj.date;
                } else if (this.status == 204) {
                    alert("Sorry, there is no map to play today.");
                }
            }
    }
    xhttp.open("GET", "/game/api/map", true);
    xhttp.send();

    var topScoreXhttp = new XMLHttpRequest;
    topScoreXhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let response = JSON.parse(this.responseText);
            document.getElementById("score").innerHTML = `Your current score is 0. Your top score for today is ${response.count}`;
        }
    }
    topScoreXhttp.open("GET", "/game/api/count", true);
    topScoreXhttp.send("");
}

function showMap(){
    var xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let newWindow = window.open();
            let encodedImg = JSON.parse(this.responseText).data;
            newWindow.document.write(`<title>Today's Map Preview</title> \n <img src="data:image/png;base64,${encodedImg}" />`);
        }
    };
    xhttp.open("GET", `/game/api/preview?date=${date}&width=${width}&height=${height}`, true);
    xhttp.send();
}

function previewMap(){
    var xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let newWindow = window.open();
            let encodedImg = JSON.parse(this.responseText).data;
            newWindow.document.write(`<title>Your Code Preview</title> \n <img src="data:image/png;base64,${encodedImg}" />`);
        }
    };
    xhttp.open("POST", `/game/api/preview?&width=${width}&height=${height}`, true);
    xhttp.send(document.getElementById("code").value);
    
}

function submit(){
    var xhttp = new XMLHttpRequest;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let response = JSON.parse(this.responseText);
            document.getElementById("score").innerHTML = `Your current score is ${response.submit_score}. Your top score for today is ${response.top_score}`;
        }
    };
    xhttp.open("POST", `/game/api/score`, true);
    xhttp.send(document.getElementById("code").value);
}
