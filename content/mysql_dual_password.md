Title: Changing a MySQL user password across multiple application instances without downtime
Date: 2020-12-09 13:40
Tags: MySQL, MySQL Dual Password
Category: MySQL 
Slug: mysql-dual-password-functionality
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: en
Description: Are you in need to change the password for a MySQL User without downtime? With the new feature on version 8.0.14, this is possible. Come check it out.
Image: /images/mysql_dual_password.png

Do you need to change the password of a MySQL user that it's being used in an application, and can't allow a single downtime? Well, MySQL 8.0.14 came with a feature called [Dual Password Support](https://dev.mysql.com/doc/refman/8.0/en/password-management.html#dual-passwords), with it you can change the password keeping the previous password as a kind of backup. That way you still can log in using the old password or can start using the new one. With that, the password change workflow it's the following.

1) Change password keeping the old one;

2) Deploy the new config to your app/cluster;

3) Discard the old password.

To change the password and keep the old one, you have the following command.

```mysql
ALTER USER 'appuser'@'localhost' IDENTIFIED BY 'new_password' RETAIN CURRENT PASSWORD;
```

To discard the old one, run the following.

```mysql
ALTER USER 'appuser'@'localhost' DISCARD OLD PASSWORD;
```

And you are done. Hope you find it as useful as I :)
