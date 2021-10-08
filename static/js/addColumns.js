var portfolio_input = document.createElement('input');

$( document ).ready(function(){

    let table = document.getElementsByTagName('table')[0];
    let head = table.rows[0];
    let watchlist_cell = head.insertCell(10);
    watchlist_cell.innerHTML = "<b> Watchlist </b>";

    let portfolio_cell = head.insertCell(11);
    portfolio_cell.innerHTML = "<b> Portfolio </b>";

    portfolio_input.type = 'hidden';
    portfolio_input.name = 'amount';
    portfolio_input.id = 'amount';



    for (row of table.tBodies[0].rows){
        let watchlist_checkBox = document.createElement('input');
        watchlist_checkBox.setAttribute('type', 'checkbox');
        let checked_symbol = row.cells[1].innerText;
        watchlist_checkBox.setAttribute('id', checked_symbol);
        watchlist_checkBox.setAttribute('class', 'star');
        let watchlist_cell = row.insertCell(row.length);
        watchlist_cell.appendChild(watchlist_checkBox);

        let portfolio_button = document.createElement('button');
        portfolio_button.setAttribute('type', 'submit');
        portfolio_button.innerHTML = 'Add';
        portfolio_button.setAttribute('onclick', 'addToPortfolio();');
        let button_id = 'portfolio_' + row.cells[0].innerHTML;
        portfolio_button.setAttribute('id', button_id);
        portfolio_button.setAttribute('value', button_id);

        let portfolio_cell = row.insertCell(row.length);
        portfolio_cell.appendChild(portfolio_button);
        };
    });



