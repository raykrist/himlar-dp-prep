import pika
import json

#sender
class MQclient(object):

    #username = 'local'
    #password = 'local'
    #host = 'mq.vagrant.iaas.intern'
    #port = 15672
    #vhost = 'access'

    def __init__(self, config):
    	self.config = config 
        credentials = pika.PlainCredentials(
            username=self.config['mq_username'],
            password=self.config['mq_password'])

        parameters = pika.ConnectionParameters(
            host=self.config['mq_host'],
            virtual_host=self.config['mq_vhost'],
            credentials=credentials)
        print config['mq_vhost']
	print config['mq_host']
	print config['mq_username']
	print config['mq_password']
        self.connection = pika.BlockingConnection(parameters)

    def get_channel(self, queue):
        channel = self.connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        return channel

    def close_connection(self):
        self.connection.close()

    def push(self, email, password, queue='access'):
        """ Example function to push message to the message queue """
        channel = self.connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        data = {
            'email': email,
            'password': password
        }
        message = json.dumps(data)
        result = channel.basic_publish(exchange='',
                                       routing_key=queue,
                                       body=message,
                                       properties=pika.BasicProperties(
                                       delivery_mode=2))
        if result:
            print "(message %s added to queue %s', message, queue)"
       #         self.logger.debug('=> message %s added to queue %s', message, queue)
        #else:
        #    self.logger.debug('=> DRY-RUN: message %s added to queue %s', message, queue)


    def __get_config(self, section, option):
        try:
            value = self.config.get(section, option)
            return value
        except ConfigParser.NoOptionError:
            self.logger.debug('=> config file section [%s] missing option %s',
                              section, option)
        except ConfigParser.NoSectionError:
            self.logger.debug('=> config file missing section %s', section)
        return None
