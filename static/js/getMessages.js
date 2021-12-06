
setInterval(function(){
    console.log(friend_id);
    $.ajax({
        type: 'GET',
        url: '/messenger/getMessages/' + friend_id,
        success: function(response){
            $('#chat_textarea').empty();

            for (var key in response.messages){
                var temp = response.messages[key];
                console.log(temp);
                $('#chat_textarea').append(temp);
            }
        },
        error: function(response){
            alert('Error')
        }
    });
}, 1000);


