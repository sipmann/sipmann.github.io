Solving java.net.SocketException: Protocol family unavailable on a Java + Docker + WildFly
###########################################################################################

:date: 2018-03-04 17:40
:tags: Java, WildFly, Docker, java.net.SocketException, Protocol family unavailable
:category: Java
:slug: socketException-protocol-family-unavailable-java-docker-wildfly
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:linkedin: sipmann
:lang: en
:related_posts: reading-files-java-readAllBytes-outofmemory
:image: images/og/java-wildfly.png
:description: Author: Maurício Sipmann, Solving java.net.SocketException when using WildFly with Docker with a simple xml tag

On the last days I've been playing with `WildFly Swarm <http://wildfly-swarm.io/>`_ and I decided to deploy a simple app with Docker. Should work fine, at least that was what I thought. Built a container with the following Dockerfile and instead of a working web app, all that I got was the error `java.net.SocketException: Protocol family unavailable`.

.. code-block:: Dockerfile

	FROM java:openjdk-8-jdk

	COPY target/issues.jar /opt/issues.jar

	EXPOSE 8080

	CMD ["java","-jar","/opt/issues.jar"]

For some reason, WildFly and Java decided to use the IPv6 network interface from Docker instead the v4, so all you have to do is tell Java to prefer IPv4 instead with the following configuration option in your pom.xml file inside your WildFly plugin.

.. code-block:: xml

	<plugin>
		<groupId>org.wildfly.swarm</groupId>
		<artifactId>wildfly-swarm-plugin</artifactId>
		<version>2018.2.0</version>

		<!-- ADD THIS -->
		<configuration>
		  <mainClass>org.wildfly.swarm.examples.netflix.ribbon.frontend.Main</mainClass>
		  <properties>
			<java.net.preferIPv4Stack>true</java.net.preferIPv4Stack>
		  </properties>
		</configuration>

 
Another way to solve is adding the same properties to the run command at the Dockerfile, so you choose where you'll add it. Bellow the Dockerfile solution.

.. code-block:: Dockerfile

	FROM java:openjdk-8-jdk
	ENV JAVA_OPTS="-Djava.net.preferIPv4Stack=true -Djava.net.preferIPv4Addresses=true"

	COPY target/issues.jar /opt/issues.jar
	
	EXPOSE 8080

	ENTRYPOINT exec java $JAVA_OPTS -jar /opt/issues.jar
