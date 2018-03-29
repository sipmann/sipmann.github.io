Connecting to a database through SSH
######################################

:date: 2018-03-29 10:03
:tags: openssh, tunnel, ssh tunnel, ssh, through firewall
:category: Linux
:slug: connecting_to_database_through_ssh
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:linkedin: sipmann
:related_posts: linux-external-display-with-disper
:description: Tunneling a database connection through ssh.
:lang: en

If someday, for some reason, you need to establish a connection with a database which is behind a firewall and you only have SSH access on that server (and you don't want to use a CLI) you can do an SSH tunnel. It's pretty simple, bellow has a sample of how to allow connections to a remote Firebird database.

.. code-block:: shell

    ssh -L 3051:192.168.1.9:3050 username@192.168.1.9


The `-L` parameter tells to SSH do a local port forwarding on local port `3051` to remote port `3050`. You can use it to a connection with many services, not just databases.

You can do the reverse kind of tunnel, forward connections from the host to your local machine, you just have to change the parameter form "-L" to "-R" and the port order is inverted, first come the port where the server will listen and after your localhost port. This remote port forwarding must be enabled on the server. Look for `GatewayPorts` at the ssh config file.

.. code-block:: shell

    ssh -R 3050:localhost:3050 username@192.168.1.9 

Why whould you need something like that?? Let's say you want to share a localhost site/database with a friend, but your internet connection don't allow you to expose any port but you have access to a remote server witch can do that. Problem solved ;).
