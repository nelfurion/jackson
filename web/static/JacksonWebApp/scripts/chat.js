(function($) {
    var CHAT_ENDPOINT = '/jackson/chat/',
        sendButton = $('#chat_btn_send'),
        chatLogContainer = $('#chat_chat_log'),
        inputField = $('#chat_user_input'),
        row = $('<div class="row"></div>'),
        input = $('<div class="pull-right"></div>'),
        output = $('<div></div>');

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

    var csrfToken = getCookie('csrftoken') || $(":input[name='csrfmiddlewaretoken']").val();

    sendButton.on('click', function(event) {
        event.preventDefault();

        var inputText = inputField.val();
        var userInput = input.clone().text(inputText);
        var newRow = row.clone();
        newRow
            .addClass('chat_user_input')
            .append(userInput);

        chatLogContainer.append(newRow);

        $.ajax({
            url: CHAT_ENDPOINT,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                user_input: inputText,
            })
        })
        .done(function(result) {
            console.log(result);
            var chatbotOutput = output.clone().text(result.answer);
            var newRow = row.clone();

            newRow
                .addClass('chatbot_output')
                .append(chatbotOutput);
            chatLogContainer.append(newRow);
        });
    });

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
    });
})(jQuery)