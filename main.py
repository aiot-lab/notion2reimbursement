from notion_client import Client
import openpyxl as xl
import datetime as dt
import shutil
import requests
import os
from loguru import logger

from Ritem import RItem, Claimant
from write_wb import write_wb_info, write_wb_item, write_wb_price

import yaml

with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# >>>>>>>>>>>>>>>>>>>>>>>>>>> Config >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
template_file = "reimbursement.xlsx"

creation_date = str(dt.datetime.now().strftime("%Y-%m-%d"))

notion = Client(auth=config["notion"]['secret_token'])
database_id = config['notion']['database_id']

claimant_name = config['claimant_name']

save_root = config["save_root"]

# >>>>>>>>>>>>>>>>>>>>>>>>>>> Init >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
items = []

hkd_price = []
rmb_price = []
map_price_dict = {
    "RMB": rmb_price,
    "HKD": hkd_price,
}

creation_date = dt.datetime.now().strftime("%Y-%m-%d")

# >>>>>>>>>>>>>>>>>>>>>>>>>>> Notion Database >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def query_database(notion, database_id, claimant_name):
    # Query the database
    results = notion.databases.query(
        **{
            "database_id": database_id,
            "filter": {
                "and": [
                    {
                        "property": "Status",
                        "select": {
                            "equals": "Delivered"
                        }},
                    {
                        "property": "PoC",
                        "select": {
                            "equals": claimant_name
                        }}]
            }
        }
    ).get("results")
    return results


if __name__ == "__main__":
    output_file = r"reimbursement_{}_{}.xlsx".format(
        claimant_name, str(creation_date))
    shutil.copyfile(template_file, output_file)
    wb = xl.load_workbook(output_file)

    results = query_database(notion, database_id, claimant_name)

    for i, result in enumerate(results):
        item_name = result["properties"]["Item"]["title"][0]["text"]["content"]
        if item_name is None:
            continue

        logger.info(f"Processing {item_name}")
        try:
            name = result["properties"]["PoC"]['select']['name']
            id = result["properties"]["Staff/Student ID"]['select']['name']
            email = result["properties"]["Email"]['email']
        except KeyError:
            raise KeyError(
                "Please check the column name of PoC, Staff/Student ID, Email")

        try:
            phone = result["properties"]["Phone"]['phone_number']
        except KeyError:
            raise KeyError("Please check the column name of Phone")

        claimant = Claimant(name=name, id=id, email=email, phone=phone)
        wb = write_wb_info(wb, creation_date, claimant)

        try:
            price = result["properties"]["Price"]["rich_text"][0]['text']['content']
            # logger.debug(f"Current: {price.split(' ')[1]}")
            # price = price.split(" ")[1] + price.split(" ")[0]
            map_price_dict[price.split(" ")[1]].append(
                float(price.split(" ")[0]))
        except KeyError:
            raise KeyError("Please check the column name of Price")
        except IndexError:
            raise IndexError(
                "Please check the price format, should be '100 HKD' or '100 RMB'")

        item = RItem(item_name=item_name, item_price=price)
        wb = write_wb_item(wb, item)

        save_folder = os.path.join(save_root, f'{creation_date}-{name}')
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        item_folder = str(item.item_idx) + "-" + item_name
        item_path = os.path.join(save_folder, item_folder)
        if not os.path.exists(item_path):
            os.makedirs(item_path)
        # logger.info(f"Get Names, ID, Email: {name}, {id}, {email}")
        logger.info(f"Item Path{item_path}")

        items.append(item)

        page_id = result['id']
        blocks = notion.blocks.children.list(block_id=page_id).get("results")
        file_idx = 0
        for block in blocks:
            block_type = block["type"]
            if block_type == "pdf":
                url = block['pdf']["file"]["url"]
                r = requests.get(url, allow_redirects=True)
                file_name = f"{item_name}_{file_idx}.pdf"
                with open(os.path.join(item_path, file_name), 'wb') as f:
                    f.write(r.content)
                file_idx += 1
            elif block_type == "image":
                url = block["image"]["file"]["url"]
                r = requests.get(url, allow_redirects=True)
                file_name = f"{item_name}_{file_idx}.jpg"
                with open(os.path.join(item_path, file_name), 'wb') as f:
                    f.write(r.content)
    hkd_price_total = sum(hkd_price)
    rmb_price_total = sum(rmb_price)

    for item in items:
        print(item)
    print(f"\033[94m HKD Total:\033[0m \033[4m{hkd_price_total}\033[0m")
    print(f"\033[94m RMB Total:\033[0m \033[4m{rmb_price_total}\033[0m")
    wb = write_wb_price(wb, hkd_price_total, rmb_price_total)
    wb.save(os.path.join(save_folder, output_file))
    os.remove(output_file)
