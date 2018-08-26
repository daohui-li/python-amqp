## Introduction

This is a python project demonstrating 
1. Python syntax
2. Its interaction with MQ using AMQP: the messages are sent to default exchange with the routine key being same as the name of the intended queue.
3. Some advanced python features such as using _contextmanager_, and _unittest_ modules

### Pre-condition

1. RabbitMQ, or other MQ, and has AMQP feature enabled; port 5672 is reserved for AMQP, and Firewall is opened for the port
2. _pika_ module is installed

### Files

#### Directory structure

| Directory | Description |
| ----- | ----- |
| src  | it contains python scripts |
| test | it contains unit test scripts |
| data | it contains configuration data |

#### Script Files

| Script | Description |
| ------ | ------ |
| my_config.py | reading configuration from a property file. |
| my_logging.py | logging utility.|
| amqp-connect.py | methods of connecting to MQ and creating a channel, as well as a _RPC_ methods. |
| amqp-receiver.py | subscribe a queue and wait for consuming messages sent from _amqp-sender.py_.  |
| amqp-sender.py | send a message to default exchange with routing key set as the queue name (so that AMQP will forward the message to the queue) |
| fib_func.py | Fibonacci function calculation. |
| fib_service.py | receives the message from a predefined queue, calculates the Fibonacci number, and then publish the answer to the queue defined in the caller's property |
| fib_client.py | create an exclusive queue for receiving answer from the server, publish a request with the information of the exclusive queue in the property, and then wait until receiving message from the exclusive queue. |


## Future works

1. Use exchange, which has three types: 
  a. _fanout_: similar to broadcast messages to all the queues attached to the exchange
  b. _direct_: similar to one-to-one communication
  c. _topic_: consumer can bind a queue to the _topic_ type exchange to receive messages whose routing key fits to the specific pattern
2. Secure the transport
3. Encrypt messages and/or add digests to the messages