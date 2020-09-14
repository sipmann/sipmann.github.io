Menu dinâmico com as apps do django
####################################

:date: 2018-01-21 21:17
:tags: python, django
:category: Python
:slug: menu-dinamico-com-apps-do-django
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:linkedin: sipmann
:related_posts: editando-o-admin-do-django
:lang: pt

Digamos que sua empresa trabalha com Django desenvolvendo aplicações cujas apps são plugaveis e reutilizáveis. Por que não se aproveitar de um certo padrão de desenvolvimento para desenvolver menus que se modificam de acordo com as apps que estão no projeto? Como o objetivo aqui não é desenvolver uma app em si, vamos utilizar um projeto com algumas de modelo. Se desejar estudar mais sobre desenvolvimento Django, a documentação é muito boa, mas também temos blogs e sites excelentes sobre o assunto.

Para conseguirmos atingir esse objetivo, vamos utilizar a api `Django.apps <https://docs.djangoproject.com/en/2.0/ref/settings/#installed-apps>`_ que está disponível a partir da versão 1.7.
Com esta api, vamos percorrer as apps e se possível, criar um link para uma URL base de cada uma delas. Para começo, baixe os fontes do `projeto aqui <https://github.com/sipmann/menusapp-django/releases/tag/v1>`_, rode o pip install do projeto e no fim, sua estrutura de pastas deve ficar como abaixo.

.. code-block:: bash

	../menusapp/
	├── comentarios
	│   ├── templates
	│   │   └── comentarios
	│   │      └── listagem.html
	│   ├── __init__.py
	│   ├── admin.py
	│   ├── apps.py
	│   ├── models.py
	│   ├── tests.py
	│   ├── urls.py
	│   └── views.py
	├── core
	│   ├── templates
	│   │   └── core
	│   │       └── base.html
	│   │       └── listagem.html
	│   ├── __init__.py
	│   ├── admin.py
	│   ├── apps.py
	│   ├── models.py
	│   ├── tests.py
	│   ├── urls.py
	│   └── views.py
	├── menusapp
	│   ├── __init__.py
	│   ├── settings.py
	│   ├── urls.py
	│   └── wsgi.py
	└── manage.py


Rode o projeto e veja como é o seu funcionamento. É na app core que temos a base do nosso HTML, então será nele que iremos trabalhar. Quando se trata de algo que será renderizado no template base, eu gosto muito de utilizar 'template tags' para facilitar. 
Neste `link <http://www.sipmann.com/editando-o-admin-do-django.html>`_ tem mais um exemplo de utilização de 'template tag' caso esteja interessado.

Vamos então criar uma pasta chamada template_tag e dentro dela a nossa tag. Vamos chamá-la de menus_tag.py. Abaixo vamos ver um pouco da nossa tag.
O código é bem simples e auto explicativo, importamos as bibliotecas necessárias e realizamos o @register da tag com o nome do template que será renderizado.
E por ultimo, retornamos uma tupla de dados para o template.

.. raw:: html

	<div class="livros">
		<div class="recomendacoes">Recomendações</div>
		<a rel="noopener" href="https://www.amazon.com.br/gp/product/8575225081/ref=as_li_ss_il?ie=UTF8&linkCode=li2&tag=sipmann-20&linkId=c17fa3ac84e734741a3761e874d7d286" target="_blank"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=8575225081&Format=_SL160_&ID=AsinImage&MarketPlace=BR&ServiceVersion=20070822&WS=1&tag=sipmann-20" ></a><img src="https://ir-br.amazon-adsystem.com/e/ir?t=sipmann-20&l=li2&o=33&a=8575225081" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
		<a rel="noopener" href="https://www.amazon.com.br/gp/product/B074ZTLKHB/ref=as_li_ss_il?ie=UTF8&linkCode=li2&tag=sipmann-20&linkId=e2f37c07da2dc4111ae47854b205d01a" target="_blank"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B074ZTLKHB&Format=_SL160_&ID=AsinImage&MarketPlace=BR&ServiceVersion=20070822&WS=1&tag=sipmann-20" ></a><img src="https://ir-br.amazon-adsystem.com/e/ir?t=sipmann-20&l=li2&o=33&a=B074ZTLKHB" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
	</div>

.. code-block:: python

    from django import template
    from django.apps import apps

    #Carrega o registro de template tags
    register = template.Library()

    #Registra o metodo a seguir como uma inclusion_tag indicando o template a ser renderizado
    @register.inclusion_tag('menus_por_app.html')
    def menus_por_app():
    	lst = apps.get_app_configs()
    	return { 'lst_apps' : lst }

O template está abaixo e é simplesmente um for percorrendo as apps e gerando uma lista com os seus menus. As outras propriedades você pode ver direto na `documentação <https://docs.djangoproject.com/en/2.0/ref/applications/#django.apps.AppConfig>`_.
Algumas ressalvas para o que foi feito por questões de praticidade para uso posterior, utilizei um with para concatenar e gerar a url e criei um apelido para a url para validar a existência da mesma. Fora isto, nada de novo.

.. code-block:: html

    {% if not lst_apps %}
			<p>Nenhuma app</p>
		{% else %}
			<ul>
				{% for app in lst_apps %}
					{% with app.name|add:":listagem" as link %}
						{% url link as the_url %}
							{% if the_url %}
							<li>
								<a href="{% url link %}">{{ app.verbose_name|truncatechars:30 }}</a>
							</li>
							{% endif %}
					{% endwith %}
				{% endfor %}
			</ul>
		{% endif %}


.. image:: /images/menu_apps.png
	:alt: Resultado final

No final, o resultado obtido deve ser semelhante ao acima. Repare que está listando as duas aplicações. E acima de tudo, repare que só serão exibidos os links cuja app tenha um namespace de mesmo nome e uma url de nome `listagem`.
A estrutura final pode ser vista abaixo. Atente-se aos nomes tanto das pastas quanto dos arquivos, pois qualquer diferença pode causar o não funcionamento.

.. code-block:: bash

	../menusapp/
	├── comentarios
	│   ├── templates
	│   │   └── comentarios
	│   │      └── listagem.html
	│   ├── __init__.py
	│   ├── admin.py
	│   ├── apps.py
	│   ├── models.py
	│   ├── tests.py
	│   ├── urls.py
	│   └── views.py
	├── core
	│   ├── templates
	│   │   └── core
	│   │   │   └── base.html
	│   │   │   └── listagem.html
	│   │   └── menus_por_app.html
	│   ├── templatetags
	│   │   ├── __init__.py
	│   │   └── menus_tag.py
	│   ├── __init__.py
	│   ├── admin.py
	│   ├── apps.py
	│   ├── models.py
	│   ├── tests.py
	│   ├── urls.py
	│   └── views.py
	├── menusapp
	│   ├── __init__.py
	│   ├── settings.py
	│   ├── urls.py
	│   └── wsgi.py
	└── manage.py


Espero que tenham gostado, críticas e sugestões são bem-vindas. `Fontes do Projeto <https://github.com/sipmann/menusapp-django/releases/tag/v2>`_
