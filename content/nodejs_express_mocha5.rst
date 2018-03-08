Testing Express.js application with Mocha 5.0 not exiting
###########################################################

:date: 2018-03-12 17:40
:tags: nodejs, expressjs, mocha5, mohca not exiting
:category: Java
:slug: testing_expressjs_with_mocha5_not_exiting
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:linkedin: sipmann
:lang: en
:status: draft

If search for nodejs apps with express and tests with mocha you will fild a bunch of tutorials, and that's cool, but almost every article cover with the tests with the version 3 or lower from Mocha. This version is OK and works well, but the `since the version 4 <https://mochajs.org/#--exit----no-exit>`_, mocha wont exit the test after it runs. 

    "Prior to version v4.0.0, by default, Mocha would force its own process to exit once it was finished executing all tests. This behavior enables a set of potential problems; it’s indicative of tests (or fixtures, harnesses, code under test, etc.) which don’t clean up after themselves properly. Ultimately, “dirty” tests can (but not always) lead to false positive or false negative results."

The way to solve this is one of the options bellow.

1. Append a cmd argument `--exit` at your mocha command

.. code-block:: shell

    mocha --exit

2. Code and `after` event at your test case that shutdown the express server (or any other server you are using)

.. code-block:: javascript

    const chai = require('chai');
    const chaiHttp = require('chai-http');
    const should = chai.should();
    
    const server = require('../server'); //your server javascript

    chai.use(chaiHttp);

    describe('/GET', () => {
        //...
    });

    after(() => {
        server.process.close();
    });
