
var height;
var width;
var date;

function init() {
    document.getElementById("code").value = "";
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
                    window.location.href = "/";
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

    document.getElementById("buttonShare").addEventListener("click", async () => {
        return $.ajax({
            url: '/game/api/count' + "?" + jQuery.param(null),
            type: 'GET',
            success: function (d) {
                let userScore = d["count"];
                navigator.clipboard.writeText(userScore);
                alert(`Copied your score of ${userScore} to the clipboard.`)
            }
        })
    })
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

function setTemplate(){
    document.getElementById("code").value = 
    `<!DOCTYPE html>
    <html lang="en">
    <head>
    <title>My Website</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <style>
    /*write your css code here*/
    </style>
    
    </head>
    
    <body>
    <!-- write your html code here -->
    </body>
    
    </html>
    `;
}
