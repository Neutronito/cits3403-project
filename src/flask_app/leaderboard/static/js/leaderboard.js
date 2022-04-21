function api_call(getRoute, request_type, success) {
    return $.ajax({
    url: base_path + getRoute,
    type: request_type,
    success: success,
    })
}

let personData = [];
let sortDirection = false;


window.onload = () => {
    api_call("/leaderboard/api/user/all", 'GET',(d) => {loadTableData(d)});
};

function loadTableData(ppersonData){
    personData = ppersonData;
    const tableBody = document.getElementById('tableData');
    let dataHtml = '';
    for(var data in personData){
        dataHtml += `<tr><td>${personData[data]["name"]}</td><td>${personData[data]["count"]}</td></tr>`;
    }
    tableBody.innerHTML = dataHtml;
}
function loadTableData(ppersonData){
    personData = ppersonData;
    const tableBody = document.getElementById('tableData');
    let dataHtml = '';
    for(var data in personData){
        dataHtml += `<tr><td>${personData[data]["name"]}</td><td>${personData[data]["count"]}</td></tr>`;
    }
    tableBody.innerHTML = dataHtml;
}

function sortData(columnName){
    const dataType = 'number';
    sortDirection = !sortDirection;
    switch(dataType){
        case 'number':
            sortNumbers(sortDirection, columnName);
            break;
    }
    loadTableData(personData);
}

function sortNumbers(sort, columnName){
    personData = personData.sort((p1,p2) =>{
        return sort ? p1[columnName] - p2[columnName] :  p2[columnName] - p1[columnName];
    })
}