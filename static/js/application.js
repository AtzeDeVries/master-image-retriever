
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/mir');
    var numbers_received = [];

    //receive details from server
    socket.on('querystatus', function(msg) {
         $('#query').html(msg.data);
    });

    socket.on('filefind', function(msg) {
           $('#filefind').html(msg.data);
    });

    socket.on('errors', function(msg) {
         $('#errors').html(msg.data);
    });

    socket.on('downloads', function(msg) {
         $('#downloads').html(msg.data);
    });

    $('form#emit').submit(function(event) {
        socket.emit('getfiles', {data: $('#emit_data').val()});
        return false;
    });

});
