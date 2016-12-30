(function($) {
    var CHAT_ENDPOINT = '/chatbot/chat/',
        sendButton = $('#chat_btn_send'),
        chatLogContainer = $('#chat_chat_log'),
        inputField = $('#chat_user_input');

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }

        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    sendButton.on('click', function(event) {
        event.preventDefault();

        var user_input = inputField.val();
        chatLogContainer.append('YOU: ' + user_input + '<br />');

        $.ajax({
            url: CHAT_ENDPOINT,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                user_input: user_input
            })
        })
        .done(function(result) {
            chatLogContainer.append('Jackson: ' + result.answer + '<br />');
        });
    });

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
})(jQuery)