Title: Apache Nifi JSON to SQL Replacing underscore
Date: 2020-12-02 19:00
Tags: Apache Nifi, ConvertJSONToSQL, replacing underscore
Category: Tools
Slug: apache-nifi-json-to-sql-replacing-underscore
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: en
Description: Apache NiFi replacing the underscore on the SQL when using translate field names property on ConvertJSONToSQL component.
Image: /images/mysql_monitorin_powershell.png
Status: draft

Recently I was doing some ETL with [Apache NiFi](https://nifi.apache.org/). But after a few minutes drawing my flow, I saw that the component ConvertJSONToSQL was replacing the underscore ('_') from the field name in the where condition (I was preparing an Update SQL). That was weird because at the set statement, the field name was kept intact. After some research I found that the property (see bellow) `Translate Field Names` was the responsible for that weird replace.

![Apache NiFi JSONToSQL config](/images/apache_nifi_jsontosql.png)

Before setting it to NO, be aware that the properties on your JSON data must be exactly the name of your fields.