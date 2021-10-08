var selected_exchange = null;

function connectExchange(){
    let dropdown = document.getElementById('exchanges_select');
    $('#exchange_input').val(dropdown.innerText);
    console.log(dropdown.innerText);

    };
