

$(document).ready(function(){

    console.log(watchlist_ids);
    let table = document.getElementsByTagName('table')[0];

    for (row of table.rows){
        if (watchlist_ids.includes(row.cells[1].innerText)){
            row.cells[10].children[0].checked = true;
        };
    };
});

