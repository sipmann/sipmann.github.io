Microservices with NodeJS, Express.js and RabbitMQ Part 1
############################################################

:date: 2018-04-04 11:25
:tags: nodejs, microservices, rabbitmq, expressjs, imagemin, imagemin-pngquant, node js
:category: front-end
:slug: microservices_nodejs_express_rabbitmq_part_1
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:linkedin: sipmann
:lang: en
:series: MICROSERVICES_NODEJS_RABBITMQ
:image: /images/microservices_rabit_pt1.png

This is the first part of a microservices development series. The service will consist of the bellow architecture, where we will expose an image optimizer service that will forward the request to a `RabbitMQ <https://www.rabbitmq.com/>`_ queue and answer with the bytecode of the optimized image. It shouldn't be a long series so let's see what we can do.

.. image:: /images/microservices_rabit_pt1.png
	:alt: Service architecture

Let's get our environment working. First, we'll need to install the libraries that we'll use.

Create a dir and initialize the nodejs application inside it (`npm init`) and then let's install the deps.

* amqplib - AMQP lib to interact with rabbitmq
* express - Do our basic rest API
* express-fileupload - easy file upload parser
* imagemin and imagemin-pngquant - our image compacter

.. code-block:: shell

    npm install --save express amqplib express-fileupload imagemin imagemin-pngquant


Now let's write the entry points for our service, we'll have two basic entry points. The path `/` that will have a welcome message, the second path will be `/upload` and this is the one that will handle the image and produce a job for our workers.

.. code-block:: javascript

    const express = require('express');
    const fileUpload = require('express-fileupload');

    //Instantiate the app and set the fileupload parser to manage files
    const app = express();
    app.use(fileUpload());

    //Our index entry point
    app.get('/', (req, res) => res.send('Hello From ImageCompacter service'));

    //The path that will handle the image file and throw them to the queue
    app.post('/upload', (req, res) => {
        //With express-fileupload we can grab the files like this
        let img = req.files.image; //"image" is the name of the input

        res.send('Not ready yet');
    });

    //Finally start the app with the given port number
    app.listen(4000, () => console.log('Example app listening on port 4000!'));

Let's check if it works, run the service with node.

.. code-block:: shell

    node index.js
    Example app listening on port 4000!

Open the browser and check if it prints our hello message when accessing `localhost:4000`. Works? Greate. Now let's work with the image and see how we do it. To optimize our image, we'll use the library imagemin and `imagemin-pngquant <https://www.npmjs.com/package/imagemin-pngquant>`_, it will be that simple for now, we'll work with rabbitmq latter.

.. code-block:: javascript

    const imagemin = require('imagemin');
    const imageminPngquant = require('imagemin-pngquant');
    //...
	
    //The path that will handle the image file and throw them to the queue
    app.post('/upload', (req, res) => {
        let img = req.files.image; //"image" is the name of the input

		imagemin.buffer(img.data, {
            plugins: [imageminPngquant()]
        })
        .then(out => {
            res.write(out,'binary');
            res.end(null, 'binary');
        });
    });
	
	//...
	
Use `Postman <https://www.getpostman.com/>`_ to test the request. To see if it will work, make a request to `http://localhost:4000/upload` with a formdata with a file. Select the "send and Download" instead of "Send" and you should have an image after that. Bellow an image of how your postman should be.

.. image:: /images/microservice_postman.png
	:alt: Postman

That's it for today, next week we'll change our code to use RabbitMQ.
