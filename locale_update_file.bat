pybabel extract -F babel.cfg -o messages.pot .

pybabel update --input-file messages.pot --output-dir translations/ --domain messages

pybabel init --input-file messages.pot --output-dir translations/ --locale pt --domain messages