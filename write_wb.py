from Ritem import RItem, Claimant
from openpyxl import Workbook


def write_wb_info(wb: Workbook, date: str, claimant: Claimant):
    sheet = wb.worksheets[0]
    sheet['C10'] = date
    sheet['F13'] = claimant.name
    sheet['E16'] = claimant.uid
    sheet['F19'] = claimant.email
    sheet['F20'] = claimant.phone
    return wb


def write_wb_item(wb: Workbook, item: RItem):
    sheet = wb.worksheets[0]
    item_idx = 1
    for row in sheet.iter_rows(min_row=24, max_row=40, min_col=0, max_col=40):
        if row[0].value is None:
            row[0].value = item.item_name
            row[9].value = item_idx
            row[10].value = item.item_price
            item.set_idx(item_idx)
            if (hasattr(item, 'account') and item.account is not None):
                account_tuple = item.account.split(".")
                row[15].value = account_tuple[0]
                row[19].value = account_tuple[1]
                row[27].value = account_tuple[2]
                row[31].value = account_tuple[3]
                row[35].value = account_tuple[4]
                row[38].value = account_tuple[5]
            break
        item_idx += 1
    return wb


def write_wb_price(wb: Workbook, hkd, rmb):
    sheet = wb.active
    sheet["K41"] = "HKD" + " " + str(hkd)
    sheet["K42"] = "CNY" + " " + str(rmb)
    return wb
