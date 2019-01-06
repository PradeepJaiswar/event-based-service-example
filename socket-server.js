var port = 8080;
var WebSocketServer = require('ws').Server;
var wss = new WebSocketServer({ port: port });

console.log('listening on port: ' + port);

/*
* Tell every connected client that new image is uploaded and resized
* Client can update them self now
*/
wss.on('connection', function connection(ws) {
    ws.on('message', function incoming(data) {
        console.log('message', data);
        try {
            wss.clients.forEach(function each(client) {
                if (client !== ws) {
                    client.send(data);
                }
            });
        }
        catch (err) {
            console.log(err.message)
        }
    });
});