import SockJS from 

// Use SockJS
Stomp.WebSocketClass = SockJS;

// Connection parameters
var mq_username = "pi_rabbit_admin",
    mq_password = "guest",
    mq_vhost    = "yPvawEVxks7MLg3lfr3g",
    mq_url      = 'http://mqtt-redesfis.ws.atnog.av.it.pt:8080/stomp',

    // The queue we will read. The /topic/ queues are temporary
    // queues that will be created when the client connects, and
    // removed when the client disconnects. They will receive
    // all messages published in the "amq.topic" exchange, with the
    // given routing key, in this case "mymessages"
    mq_queue    = "/topic/mymessages";


// This is where we print incomoing messages
var output;

// This will be called upon successful connection
function on_connect() {
  output.innerHTML += 'Connected to RabbitMQ-Web-Stomp<br />';
  console.log(client);
  client.subscribe(mq_queue, on_message);
}

// This will be called upon a connection error
function on_connect_error() {
  output.innerHTML += 'Connection failed!<br />';
}

// This will be called upon arrival of a message
function on_message(m) {
  console.log('message received'); 
  console.log(m);
  output.innerHTML += m.body + '<br />';
}

// Create a client
var client = Stomp.client(mq_url);

window.onload = function () {
  // Fetch output panel
  output = document.getElementById("output");

  // Connect
  client.connect(
    mq_username,
    mq_password,
    on_connect,
    on_connect_error,
    mq_vhost
  );
}
