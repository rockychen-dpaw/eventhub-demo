<!doctype html>
<head>
    <meta charset="utf-8" />
    <title>WebSocket Chat</title>

    <style>
        li { list-style: none; }
    </style>

    <script src="/static/js/jquery-3.4.1{{"" if debug else ".min" }}.js"></script>
    <script>
        $(document).ready(function() {
            if (!window.WebSocket) {
                if (window.MozWebSocket) {
                    window.WebSocket = window.MozWebSocket;
                } else {
                    $('body').html("<h1>Your browser doesn't support WebSockets.</h1>");
                }
            }
        })

        function publish(publisher,event_type,payload) {
            $.ajax({
                type:'POST',
                url:'/publish',
                data:{publisher:publisher,event_type:event_type,payload:payload},
                success:function(data,status,jqXHR){},
                error:function(xhr,status,message){
                    alert(xhr.status + " : " + (xhr.responseText || message))
                },
                xhrFields: {
                    withCredentials: true
                }

            })
        }

        function listen(subscriber,publisher,event_type){
            ws = new WebSocket('wss://' + window.location.host + '/listen/' + subscriber + '/' + event_type);
            ws.onopen = function(evt) {
                $("#id_" + subscriber + "_" + publisher + "_" + event_type + "_status").html("Listening")
                $("#id_" + subscriber + "_" + publisher + "_" + event_type + "_listen").prop("disabled",true)
                $("#id_" + subscriber + "_" + publisher + "_" + event_type + "_stoplisten").prop("disabled",false)
            }
            ws.onmessage = function(evt) {
                $("#id_" + subscriber + "_" + publisher + "_" + event_type).prepend($(evt.data))
                $("#id_" + subscriber + "_" + publisher + "_" + event_type).scrollTop(0)
            }
            ws.onclose = function(evt) {
                $("#id_" + subscriber + "_" + publisher + "_" + event_type + "_status").html("")
                $("#id_" + subscriber + "_" + publisher + "_" + event_type + "_listen").prop("disabled",false)
                $("#id_" + subscriber + "_" + publisher + "_" + event_type + "_stoplisten").prop("disabled",true)
            }
        }

        function stopListen(subscriber,publisher,event_type){
            $.ajax({
                type:'GET',
                url:'/stoplisten/' + subscriber + '/' + event_type,
                success:function(data,status,jqXHR){},
                error:function(xhr,status,message){
                    alert(xhr.status + " : " + (xhr.responseText || message))
                },
                xhrFields: {
                    withCredentials: true
                }

            })
        }

    </script>
</head>
<body>
    <h2>Event hub publish/subscribe demo app</h2>
    <table>
    % for publisher,event_types in event_tree:
        % for event_type,subscribers in event_types:
        <tr>
          <th>{{publisher.name}}.{{event_type.name}}</th>
          <td>
             <input type="text" id="id_{{publisher.name}}_{{event_type.name}}">
             <button name="publish" onclick="publish('{{publisher.name}}','{{event_type.name}}',$('#id_{{publisher.name}}_{{event_type.name}}').val())">Publish</button>
          </td>
          <td>
            <table>
            <tr>
            % for subscriber in subscribers:
              <th>
                {{subscriber.name}}
                <button id="id_{{subscriber.name}}_{{publisher.name}}_{{event_type.name}}_listen"  onclick="listen('{{subscriber.name}}','{{publisher.name}}','{{event_type.name}}')">Listen</button>
                <button id="id_{{subscriber.name}}_{{publisher.name}}_{{event_type.name}}_stoplisten" disabled onclick="stopListen('{{subscriber.name}}','{{publisher.name}}','{{event_type.name}}')">Stop</button>
                <br><div id="id_{{subscriber.name}}_{{publisher.name}}_{{event_type.name}}_status"></div>
              </th>
            % end
            </tr>
            <tr>
            % for subscriber in subscribers:
              <td><div id="id_{{subscriber.name}}_{{publisher.name}}_{{event_type.name}}" style="width:600px;height:200px;background-color:#e2efcd;overflow:scroll"></div></td>
            % end
            </tr>
            </table>
           </td>
        </tr>
        % end
    % end
    </table>
</body>
</html>
