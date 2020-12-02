Title: Changing a MySQL user password acros multiple application instances
Date: 2020-10-14 19:00
Tags: MySQL, MySQL Dual Password
Category: PowerShell 
Slug: mysql-dual-password-functionality
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: en
Status: Draft
Description: Monitoring a MySQL replication with PowerShell, sending e-mails and even more to warn you about the replica state.
Image: /images/mysql_monitorin_powershell.png

Do you need to change the password of a MySQL user that it's being used in an application, and can't allow a single downtime? Well, MySQL 8.0.14 came with a feature called [Dual Password Support](https://dev.mysql.com/doc/refman/8.0/en/password-management.html#dual-passwords), with it you can change the password keeping the previous password as a kind of backup. That way you still can login using the old password, or can start using the new one. With that, the password change workflow it's the following.

1) Change password keeping the old one.

2) Deploy the new config to your app/cluster.

3) Discard the old password.

To do that, you have the following command.

```mysql
ALTER USER 'appuser'@'localhost' IDENTIFIED BY 'new_password' RETAIN CURRENT PASSWORD;
```

To discard the old one, run the following.

```mysql
ALTER USER 'appuser'@'localhost' DISCARD OLD PASSWORD;
```

And you are done. Hope you find it as useful as I :)

Force build