Title: Apache Nifi JSON to SQL removendo underline
Date: 2020-12-02 14:00
Tags: Apache Nifi, ConvertJSONToSQL, removendo underline
Category: Tools
Slug: apache-nifi-json-to-sql-replacing-underscore
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: pt
Description: Apache NiFi substituindo o underline na SQL quando utilizado a propriedade translate field names no componente ConvertJSONToSQL.


Recentemente eu estava desenvolvendo alguns processos de ETL com o Apache NiFi. Mas após alguns minutos desenhando o meu fluxo, eu vi um comportamento estranho do componente ConvertJSONToSQL, que estava substituindo os underline ('_') do nome de um campo utilizado na condição da SQL (eu estava preparando um UPDATE). Aquilo estava estranho, uma vez que na definição do SET da SQL, o nome do campo permanecia inalterado. Depois de algumas pesquisas, achei uma doc que a propriedade (veja abaixo) `Translate Field Names` era a responsável por este comportamento estranho.

![Apache NiFi JSONToSQL config](/images/apache_nifi_jsontosql.png)

Antes de definir a propriedade como **FALSE**, esteja ciente que as propriedades do seu JSON devem ser exatamente iguais aos nomes dos campos da sua tabela.
