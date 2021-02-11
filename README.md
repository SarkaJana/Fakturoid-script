# FAKTUROID 

Fakturoid script passes the jira.csv to fakturoid.cz to create an invoice.

To run the script you need: 
  - `--api_key` api_key to authorize  
  - `--path` path to jira.csv
  - `--email` your e-mail address connected with your fakturoid.cz account
  
All these 3 arguments are passed using the command line, see example below:

```
python jira_to_fakturoid_import.py --path /path/to/your/jira.csv --api_key 7bexxxxxxxyyyyyyyyyyyyyyyb --email your@email.cz
```
