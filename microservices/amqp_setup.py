import pika

hostname = "localhost" # default hostname
port = 5672 # default port
# connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600, 
))

channel = connection.channel()

# Set up the exchange if the exchange doesn't exist
# - use a 'topic' exchange to enable interaction
exchangename="property_management"
exchangetype="topic"
channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)


############   Error queue   #############
#declare Error queue
queue_name = 'Error'
channel.queue_declare(queue=queue_name, durable=True) 

#bind Error queue
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='*.error') 
    # bind the queue to the exchange via the key
    # any routing_key with two words and ending with '.error' will be matched

############   Notification queue    #############
#delcare Notification queue
queue_name = 'Notification'
channel.queue_declare(queue=queue_name, durable=True)

#bind Notification queue
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='*.notification') 
    # bind the queue to the exchange via the key
    # any routing_key with two words and ending with '.notification' will be matched
    

"""
This function in this module sets up a connection and a channel to a local AMQP broker,
and declares a 'topic' exchange to be used by the microservices in the solution.
"""
def check_setup():
    # The shared connection and channel created when the module is imported may be expired, 
    # timed out, disconnected by the broker or a client;
    # - re-establish the connection/channel is they have been closed
    global connection, channel, hostname, port, exchangename, exchangetype

    if not is_connection_open(connection):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, heartbeat=3600, blocked_connection_timeout=3600))
    if channel.is_closed:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)


def is_connection_open(connection):
    # For a BlockingConnection in AMQP clients,
    # when an exception happens when an action is performed,
    # it likely indicates a broken connection.
    # So, the code below actively calls a method in the 'connection' to check if an exception happens
    try:
        connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False
