
setInterval(function(){
    console.log(friend_id);
    $.ajax({
        type: 'GET',
        url: '/messenger/getMessages/' + friend_id,
        success: function(response){
            $('#chat_textarea').empty();
            console.log(response);
            for (var key in response.messages){
                var temp = "<div class='container darker'>" + response.messages[key] + "</div>"
                $('#chat_textarea').append(temp);
            }
        },
        error: function(response){
            alert('Error')
        }
    });
}, 1000);


