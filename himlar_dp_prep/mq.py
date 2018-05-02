import pika

channel = None

def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    # Open a channel
    connection.channel(on_channel_open)

def on_channel_open(new_channel):
    """Called when our channel has opened"""
    global channel
    channel = new_channel
    channel.queue_declare(queue="access", durable=True, callback=on_queue_declared)

def on_queue_declared(frame):
    """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
    channel.basic_consume(handle_delivery, queue='test')

def handle_delivery(channel, method, header, body):
    """Called when we receive a message from RabbitMQ"""
    print(body)

parameters = pika.ConnectionParameters()
connection = pika.SelectConnection(parameters, on_connected)

try:
    connection.ioloop.start()
except KeyboardInterrupt:
    connection.close()
    connection.ioloop.start()
