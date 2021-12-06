


function setScroll(){
    var $textarea = $('#chat_textarea');
    $textarea.scrollTop($textarea[0].scrollHeight);
}

function getMessages(){
    console.log(friend_id);
    $.ajax({
        type: 'GET',
        url: '/messenger/getMessages/' + friend_id,
        success: function(response){

            /* $('#chat_textarea').empty(); */
            let chatarea = document.getElementById('chat_textarea');
            chatarea.value = '';
            for (var key in response.messages){
                var temp = response.messages[key];
                console.log(temp);
                let msg = temp.timestamp + ' ' + temp.sender_id + ': ' + temp.content + '\n';
                console.log(msg);
                chatarea.value += msg;
            }
            setScroll();
        },
        error: function(response){
            alert('Error')
        }
    });
}

$(document).ready(function(){
    getMessages();
    setInterval(getMessages, 5000);
    }
);






