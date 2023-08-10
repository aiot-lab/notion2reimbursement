# Notion to Reimbursement
Since we are using Notion as our productive tool, I write a Python script to faciliate the procedure of reimbursement and connect our Notion page to reimbursement form.

See our Notion page for more details.
##  Install and config
Currently, You have to download the code and install the necessary packages. (maybe later we can host a cloud service). I assume you have set up the conda environment. Normally, we need three packages

```bash
pip install openpyxl
pip install loguru
pip install notion_client
```

Before running the code, you have first enter your info. Copy `config-template.yaml` to `config.yaml` .

```yaml
notion:
  secret_token: <your_secret_token>
  database_id: <your_database_id>
claimant_name: <your name>
save_root: <save location>
```

See our Notion Page for details.

**It will duplicate the template file, fill all your information, calculate the total prices by currency and save the proof of payment correspondingly.**

## Result

It will create a folder in your `save_root`. Here is an example:
'''yaml
├── 2023-08-11-<your_name>
│   ├── 1-Wellue ECG
│   │   ├── Wellue ECG_0.pdf
│   │   └── Wellue ECG_1.jpg
│   ├── 2-Polar H10 
│   │   ├── Polar H10 _0.pdf
│   │   └── Polar H10 _1.jpg
│   └── reimbursement_<your_name>_2023-08-11.xlsx
'''

