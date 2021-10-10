
var currency = "{{ currencies.0 }}";

$(document).ready(function(){
    let curr_list = currencies;

    let cell = document.getElementsByTagName('table')[0].rows[0].cells[1];

    let select = document.createElement('select');

    for (curr of curr_list){
        console.log(curr);

        let option = document.createElement('option')
        option.setAttribute('id', curr);
        option.setAttribute('value', curr);

        select.appendChild(option);
    }
    cell.innerHTML = select;

})

function changeFXCurrency(){
    let dropdown = document.getElementById('currency_select');
    let new_curr = dropdown.selectedOptions[0].text;
    let url = 'http://127.0.0.1:8000/markets/forex/?currency=' + new_curr;
    window.open(url, '_self');
}


