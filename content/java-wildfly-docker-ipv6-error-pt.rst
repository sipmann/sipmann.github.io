Resolvendo java.net.SocketException: Protocol family unavailable em Java + Docker + WildFly
#################################################################################################

:date: 2018-03-04 17:40
:tags: Java, WildFly, Docker, java.net.SocketException, Protocol family unavailable
:category: Java
:slug: socketException-protocol-family-unavailable-java-docker-wildfly
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:linkedin: sipmann
:lang: pt
:related_posts: reading-files-java-readAllBytes-outofmemory
:image: images/og/java-wildfly.png
:description: Resolvendo java.net.SocketException quando utilizando WildFly com Docker com uma  simples tag xml

Nos últimos dias eu estou brincando com o `WildFly Swarm <http://wildfly-swarm.io/>`_ e decidi fazer o deploy de uma aplicação simples com Docker. Deveria funcionar bem, ao menos é o que pensava. Construí um container com o seguinte Dockerfile e ao invés de obter uma aplicação web, tudo que eu obtive foi o erro `java.net.SocketException: Protocol family unavailable`.

.. code-block:: Dockerfile

	FROM java:openjdk-8-jdk

	COPY target/issues.jar /opt/issues.jar

	EXPOSE 8080

	CMD ["java","-jar","/opt/issues.jar"]

Por alguma razão, WildFly e Java, ambos decidiram utilizar um protocolo IPv6 na interface de rede no Docker invés da v4, então tudo que você tem que fazer é falar ao Java que deve dar preferência em utilizar o IPv4 com a seguinte configuração no seu arquivo pom.xml dentro da tag do plugin WildFly.

.. code-block:: xml

	<plugin>
		<groupId>org.wildfly.swarm</groupId>
		<artifactId>wildfly-swarm-plugin</artifactId>
		<version>2018.2.0</version>

		<!-- ADICIONE ISTO -->
		<configuration>
		  <mainClass>org.wildfly.swarm.examples.netflix.ribbon.frontend.Main</mainClass>
		  <properties>
			<java.net.preferIPv4Stack>true</java.net.preferIPv4Stack>
		  </properties>
		</configuration>

 
Outra forma de solucionar o problema, é adicionando a mesma propriedade ao comando de run no seu Dockerfile. Então, fica a seu critério onde adicionar. Abaixo a solução utilizando o Dockerfile.

.. code-block:: Dockerfile

	FROM java:openjdk-8-jdk
	ENV JAVA_OPTS="-Djava.net.preferIPv4Stack=true -Djava.net.preferIPv4Addresses=true"

	COPY target/issues.jar /opt/issues.jar
	
	EXPOSE 8080

	ENTRYPOINT exec java $JAVA_OPTS -jar /opt/issues.jar
