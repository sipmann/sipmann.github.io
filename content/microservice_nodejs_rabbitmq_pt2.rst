Microservices with NodeJS, Express.js and RabbitMQ Part 2
############################################################

:date: 2018-04-13 13:00
:tags: nodejs, microservices, rabbitmq, expressjs, imagemin, imagemin-pngquant, node js
:category: front-end
:slug: microservices_nodejs_express_rabbitmq_part_2
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:linkedin: sipmann
:lang: en
:series: MICROSERVICES_NODEJS_RABBITMQ
:image: /images/microservices_rabit_pt1.png

If you haven't read the `part 1 <https://www.sipmann.com/microservices_nodejs_express_rabbitmq_part_1-en.html>`_ go ahead and read it... It can be useful :). Or if for some reason you want to start now, you can grab the project where we stopped `here <https://github.com/sipmann/imagecompacter/releases/tag/v1>`_ and get along. On this part, we'll implement the RabbitMQ queue and see how we can get the best of our app and server with that.

Before we began coding, let's understand why we are going to use RabbitMQ if what we have now works? If you check again, you'll see how long it takes to answer the request with the optimized image. It takes a few seconds, so imagine an online service with thousands of request to optimize images (like `TinyPNG <https://tinypng.com/>`_) how long is it gonna take to answer every request? How much of your server is it gonna take? With only one service running, probably the server will crash. 

With a queue, we can schedule the requests so we can use the amount of memory and processor that our server has, without taking more than we can. It's better to take a few seconds to answer the request then throw some error to the user. Want more? With RabbitMQ we can see how the queue is doing and we can add more consumers (workers) to it and get things done quicker and distribute the job.

First of all, we need an up and running Rabbit server, for the sake of simplicity, I'll use a Docker container with it inside.

.. code-block:: shell

    docker run -d --name rabbit -p 5672:5672 -p 8080:15672 rabbitmq:3-management

You can see that we're running the rabbitmq:3-management image, which provides us a web interface to see how things are going. After that, if you look at our code you'll see that all the job is made at the '/upload' route, and that's what we'll change.

First, we need to understand what we need from RabbitMQ. We need something that, we send an image to a queue and get an optimized image back from that. There is a name for that, is RPC (remote procedure call) and there are two ways of doing this with rabbit. Both the ways you can see on their tutorial page. We'll use the approach that uses a global channel whose id is randomly generated (you'll use the name 'amq.rabbitmq.reply-to' but the rabbit will do the job).

Let's start importing the library, defining a few variables and defining a init function that will establish a connection with the rabbit server and create our RPC queue. The RPC queue it's where we'll receive the answer from the consumer (our worker).

.. code-block:: javascript

    //import the library
    const amqplib = require('amqplib');

    //queue channel
    let channel = null;
    //queue name
    const QUEUE = 'optimizeimg';
    
    //...

    function init() {
        return require('amqplib').connect('amqp://localhost')
            .then(conn => conn.createChannel())
            .then(ch => {
                channel = ch;
                
                //this queue is a "Direct reply-to" read more at the docs
                //When some msg comes in, we "emit" a message to the proper "correlationId" listener
                ch.consume('amq.rabbitmq.reply-to', msg => eventEmitter.emit(msg.properties.correlationId, msg.content), {noAck: true});
            });
    }

    //Random id generator
    function randomid() {
        return new Date().getTime().toString() + Math.random().toString() + Math.random().toString();
    }

    app.post('/upload', (req, res) => {
        let img = req.files.image;

        let id = randomid();

        //Event listener that will fire when the proper randomid is provided
        eventEmitter.once(id, msg => {
            res.write(msg, 'binary');
            res.end(null, 'binary');
        });

        //Checks if the queue exists, and create it if needed.
        channel.assertQueue(QUEUE)
            //Sent the buffered img to the queue with the ID and the responseQueue
            .then(() => channel.sendToQueue(QUEUE, img.data, {correlationId:id, replyTo: 'amq.rabbitmq.reply-to'}));

    });

    //Finally start the app with the given port number
    //now we initialize the rabbitmq connection before start the server
    init()
        .then(() => app.listen(4000, () => console.log('Example app listening on port 4000!')))
        .catch(err=>console.error(err));
    
Ok, now we have our server code rewritten so let's see our worker code. Create a file named 'worker.js' and let's see how it's gonna be. It's really simple. You initialize a connection with RabbitMQ too, create a channel, check if the queue exists and start watching for incoming messages. When an image arrives, we do the job with it and send back to the "replyTo" queue the optimized image for the proper sender (correlationId). In the end, we do an acknowledge of the message so it get's out from the queue.

.. code-block:: javascript

    const imagemin = require('imagemin');
    const imageminPngquant = require('imagemin-pngquant');

    let channel = null;
    const QUEUE = 'imgqueue';

    require('amqplib').connect('amqp://localhost')
    .then(conn =>conn.createChannel())
    .then(ch => {
        ch.assertQueue(QUEUE)
        .then(() => {
            //Watch incomming messages
            ch.consume(QUEUE, msg => {
                imagemin.buffer(msg.content, {
                    plugins: [imageminPngquant()]
                })
                .then(out => {
                    //Send back to the sender (replyTo) queue and give the correlationId back
                    //so we can emit the event.
                    ch.sendToQueue(msg.properties.replyTo, out, {
                        correlationId: msg.properties.correlationId
                    });

                    //Acknowledge the job done with the message. 
                    ch.ack(msg);
                });
            });
        });
    });

The key points here are. Open just one connection to the hole server. You CAN create one channel for every request that you receive, but it can take some time if you have a really big cluster of RabbitMQ. It was a quick tutorial, but I hope that it was able to clear a few questions that you might have when working with rabbit and express.
