<!doctype html>
<head>
    <meta charset="utf-8" />
    <title>WebSocket Chat</title>

    <style>
        li { list-style: none; }
    </style>

    <script src="/js/jquery-3.4.1{{"" if debug else ".min" }}.js"></script>
    <script>
        $(document).ready(function() {
            if (!window.WebSocket) {
                if (window.MozWebSocket) {
                    window.WebSocket = window.MozWebSocket;
                } else {
                    $('body').html("<h1>Your browser doesn't support WebSockets.</h1>");
                }
            }
        }
        /*
            ws = new WebSocket('ws://' + window.location.host + '/websocket');
            ws.onopen = function(evt) {
                $('#messages').append('<li>Connected to chat.</li>');
            }
            ws.onmessage = function(evt) {
                $('#messages').append('<li>' + evt.data + '</li>');
            }
            $('#send-message').submit(function() {
                ws.send($('#name').val() + ": " + $('#message').val());
                $('#message').val('').focus();
                return false;
            });
        */
    </script>
</head>
<body>
    <h2>Event hub publish/subscribe demo app</h2>
    % for publisher,event_types in event_tree:
        {{publisher.name}}
    % end
</body>
</html>
