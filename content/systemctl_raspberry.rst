Scripts de inicialização no raspberry pi
##############################

:date: 2017-11-20 18:00
:tags: Shell, raspberry
:category: Shell
:slug: script-de-inicializacao-raspberry
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:status: draft

Instalei essa semana o gitea_ no meu raspberry pi B + e queria iniciar ele no boot... Não sou profundo conhecedor de linux, então logo não sabia como fazer da melhor forma isto.
As versões atuais do Raspbian utilizam o `systemd` para gerenciar os serviços, confesso que nunca havia utilizado o systemctl para nada.

Vamos começa criando um arquivo de serviço dentro da pasta `/etc/systemd/system`, vale ressaltar que a pasta `system` deve (em teoría) ser reservada para pacotes do sistema.
Vamos criar o arquivo com o nome `gitea.service` dentro da pasta antes mencionada. Abaixo podemos ver como ficou o arquivo e um detalhamento após ele.

.. code-block:: bash
  [Unit]
  Description=Gitea Service
  After=network.target

  [Service]
  Type=simple
  User=root
  WorkingDirectory=/root/
  ExecStart=/root/gitea web
  Restart=on-abort

A composição do arquivo é bem simples, mas vamos a alguns detalhes. `Type` possui várias opções (simple, forking, oneshot), utilizamos `simple` uma vez que o nosso processo executara, permanecerá rodando e não executa um fork de processo.
Fork como acabo de comentar, deve ser utilizado caso o processo que for executando disparar mais processos. User irá definir o usuário do processo. `WorkingDirectory` definira onde o processo tera a sua base de execução, como o gitea esta localizada na pasta root,
aponto para lá. O ExecStart é bem simples e direto, deve chamar a execução do processo passando parametros caso seja necessário. O `Restart` é o que nos garantirá que o serviço permanecerá rodando caso haja algum imprevisto (exceto o fato de um usuário chamar o stop).

Salvo o arquivo la, vamos rodar um refresh para o SO perceber o novo serviço,assim rodamos `systemctl daemon-reload`. Sempre que alterarmos um serviço ou criarmos um novo, este comando deve ser executado, caso contrário o próprio systemctl pode lhe alertar de nacessidade.
Após reacarregar os serviços, vamos habilitar o serviço que criamos rodando `systemctl enable gitea`, feito isto temos alguns comandos uteis. 

* systemctl start gitea
* systemctl stop gitea
* systemctl status gitea

O comando de status pode ser visto como exemplo abaixo.

.. code-block:: bash
  ● gitea.service - Gitea Service
    Loaded: loaded (/etc/systemd/system/gitea.service; enabled; vendor preset: enabled)
    Active: active (running) since Wed 2017-10-04 00:37:34 UTC; 52min ago
  Main PID: 1087 (gitea)
    CGroup: /system.slice/gitea.service
            └─1087 /root/gitea web

  Oct 04 00:38:31 gitserver gitea[1087]: [Macaron] 2017-10-04 00:38:31: Completed /explore/users 200 OK in 80.106173ms
  Oct 04 00:38:31 gitserver gitea[1087]: [Macaron] 2017-10-04 00:38:31: Started GET /img/favicon.png for 192.168.1.4
  Oct 04 00:38:31 gitserver gitea[1087]: [Macaron] [Static] Serving /img/favicon.png

Após estes processos, você pode reiniciar seu raspberry que o gite irá subir e funcionar. Ressalto que, preste atenção tanto no `WorkingDirectory` quanto no `ExecStart`, no caso do gitea, ele utiliza o workingdir e a forma de start para saber onde irá largar os arquivos por padrão, então ou você configura ele com caminhos absolutos ou cuida na forma de start (ao menos é o que consegui pegar até agora).

.. _gitea: https://gitea.io
