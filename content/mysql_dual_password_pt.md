Title: Trocando a senha de um usuário do MySQL sem downtime da aplicação
Date: 2020-12-09 13:40
Tags: MySQL, MySQL Dual Password
Category: MySQL 
Slug: mysql-dual-password-functionality
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: pt
Description: Trocando a senha de um usuário do MySQL sem downtime da aplicação? Com a nova feature da versão 8.0.14 isso é possível. Venha conferir como.
Image: /images/mysql_dual_password.png

Você precisa trocar a senha de um usuário do MySQL que está sendo utilizado por uma aplicação e não sofrer nenhum downtime? Bom, a versão 8.0.14 do MySQL foi liberada com uma feature chamada [Dual Password Support](https://dev.mysql.com/doc/refman/8.0/en/password-management.html#dual-passwords), com esta feature você pode alterar a senha de um usuário mantendo a anterior ainda funcionando como uma forma de "backup". Desta forma você ainda conseguirá autenticar com o usuário utilizando tanto a nova senha quanto a anterior. Com isto, o seu processo de troca de senha, fica algo como:

1) Troque a senha mantendo a anterior.

2) Faça o Deploy da nova configuração na sua aplicação/cluster.

3) Descarte a senha anterior.

Para alterar a senha mantendo a anterior, você deve rodar o seguinte comando:

```mysql
ALTER USER 'appuser'@'localhost' IDENTIFIED BY 'new_password' RETAIN CURRENT PASSWORD;
```

Para descartar a senha antiga, rode o seguinte:

```mysql
ALTER USER 'appuser'@'localhost' DISCARD OLD PASSWORD;
```

E pronto. Espero que você ache isto tão útil quanto eu :)
