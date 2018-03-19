Scaffolding a React app with Parcel and Yeoman
#################################################

:date: 2018-03-17 13:00
:tags: nodejs, yeoman, parcel, react
:category: Front-end
:slug: scaffolding_react_app_with_parcel_yeoman
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:linkedin: sipmann
:lang: en
:image: /images/og/yo-reac-gen.png
:description: Author: Maurício Sipmann, I created a React + Parcel generator for Yeoman. Now you can scaffold a React app with SASS and React Router in a few seconds

Since `Parcel JS <https://parceljs.org/>`_ arrived, I've been using it a lot as an awesome alternative for WebPack. Webpack isn't bad but IMO it's too complex for the job and parcel do the same (at least the basic) with almost zero configuration. But if you need to create many apps (like a react app) over and over again, it get's a lil boring following the basic steps.

.. code-block:: shell

    npm init -y
    npm install --save react
    npm install --save react-dom
    npm install --save-dev parcel-bundler
    npm install --save-dev babel-preset-env
    npm install --save-dev babel-preset-react

    #create .babelrc file
    #create html, css, jsx files

    parcel index.html

It's not a hard job, a simple shell script do the job, but what if you need some IFs when creating the app, or even change a few things at the `package.json`? A shell script still does the job, but come on... There is a better way. `Yeoman <http://yeoman.io/>`_ is here for you. I've already `talked about it <{filename}/desenvolvendo_app_firefoxos.md>`_ on another post (Portuguese post). 

Straight to the point, I've released a Yeoman generator to get the things a lil quicker. The name is `generator-parcel-react <https://www.npmjs.com/package/generator-parcel-react>`_ and it still lacks a few things that I will deal with soon. It's pretty simple to use it.

.. code-block:: shell
    
    #First time only
    npm install -g yo
    npm install -g generator-parcel-react

    #every time you create a new app
    yo parcel-react

And that's it. Right now you can scaffold and app with React, SASS and React Router. Hope you like it and feel free to ask new features.
