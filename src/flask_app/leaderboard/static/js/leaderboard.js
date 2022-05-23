function api_call(getRoute, request_type, success) {
    return $.ajax({
    url: getRoute,
    type: request_type,
    success: success,
    })
}

let personData = [];
let sortDirection = false;
let tabType = 'total'

window.onload = () => {
    var tabEl = document.querySelectorAll('button[data-bs-toggle="tab"]')
    tabEl.forEach((t) =>{
        t.addEventListener('show.bs.tab', function (event) {
            tabType = event.target.getAttribute("data-cits3403-leaderboard-type")
            populateData()
        })
    })
    populateData();
};

function populateData() {
    api_call("/leaderboard/api/" + tabType, 'GET',(d) => {loadTableData(d)})
}


function loadTableData(ppersonData){
    personData = ppersonData;
    const tableBody = document.getElementById('tableData-'+tabType);
    let dataHtml = '';
    for(var data in personData){
        dataHtml += `<tr>`
        if (tabType === "all"){
            dataHtml += `<td>${personData[data]["date"]}</td>`
        }
        dataHtml += `<td>${personData[data]["name"]}</td><td>${personData[data]["count"]}</td>`;
        dataHtml += `</tr>`
    }
    tableBody.innerHTML = dataHtml;
}

function sortData(columnName, dataType){
    sortDirection = !sortDirection;
    switch(dataType){
        case 'number':
            sortNumbers(sortDirection, columnName);
            break;
        case 'string':
            sortStrings(sortDirection, columnName);
            break;
    }
    loadTableData(personData);
}

function sortNumbers(sort, columnName){
    personData = personData.sort((p1,p2) =>{
        return sort ? p1[columnName] - p2[columnName] :  p2[columnName] - p1[columnName];
    })
}

function sortStrings(sort, columnName) {
    personData = personData.sort((p1, p2) => {
        return sort ? p1[columnName].localeCompare(p2[columnName]): p2[columnName].localeCompare(p1[columnName])
    });
}
