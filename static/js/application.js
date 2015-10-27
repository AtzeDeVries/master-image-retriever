
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/mir');
    var numbers_received = [];

    //receive details from server
    socket.on('newnumber', function(msg) {
        //console.log("Received number" + msg.number);
        // //maintain a list of ten numbers
        // if (numbers_received.length >= 5){
        //      numbers_received.shift()
        // }
        //  numbers_received.push(msg.number);
        //  numbers_string = '';
        //  for (var i = 0; i < numbers_received.length; i++){
        //      numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        //  }
         $('#query').html(msg.number);
        //document.getElementById("querystatus").innerHTML = '' + msg.number ;
    });

    socket.on('filefind', function(msg) {
        //console.log("Received number" + msg.number);
        // //maintain a list of ten numbers
        // if (numbers_received.length >= 5){
        //      numbers_received.shift()
        // }
        //  numbers_received.push(msg.number);
        //  numbers_string = '';
        //  for (var i = 0; i < numbers_received.length; i++){
        //      numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        //  }
         $('#filefind').html(msg.data);
        //document.getElementById("querystatus").innerHTML = '' + msg.number ;
    });
});
