Could not open connection with MySQL and Hibernate
###################################################

:date: 2018-03-09 12:35
:tags: Java, MySQL, Hibernate
:category: Java
:slug: cloud-not-open-connection-java-mysql-hibernate
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:linkedin: sipmann
:lang: en
:related_posts: socketException-protocol-family-unavailable-java-docker-wildfly
:image: images/og/mysql-permission.png
:description: Author: Maurício Sipmann, How allow a remote connection on a MySQL server.

Last day I decided to deploy a MySQL Docker image to work with my Java application. I've been using PostgreSQL instead and have no problems at all, but after I moved to MySQL, the app didn't connect anymore with the database and throw some "Could not open connection" at my face, but why? I've tried to connect to it manually and got the same problem.

After some research, I found that the true error should be java.sql.SQLException: null, message from server: "Host '172.17.0.4' is not allowed to connect to this MySQL server" but it wasn't showing to me...

After all, be aware that with the docker image MySQL:5.7.21 (latest version right now) the root user isn't allowed to remote connect to the database (it's alright, security reasons) and if you still want to do remote connections to it with root there are a few things you can do.

1) Create a user or allow root to access from other IPs.

.. code-block:: SQL


	#No access to user root on any other IP
	SELECT User, Host FROM mysql.user;
	+---------------+-----------+
	| User          | Host      |
	+---------------+-----------+
	| healthchecker | localhost |
	| root          | localhost |
	+---------------+-----------+
	2 rows in set (0.01 sec)
	
	CREATE USER 'newuser'@'%' IDENTIFIED BY 'password'; #% mean any IP
	GRANT ALL PRIVILEGES ON *.* TO 'newuser'@'%';   #*.* mean database.table ;)


2) Use MariaDB instead, witch come (at least on the version 10.2.13) with root allowed to do remote connections and will work like MySQL :)

I changed to `MariaDB <https://mariadb.org/>`_ as it work without creating user or any changes on the Java code or the `docker run command`.
