class Claimant:
    def __init__(self, name=None, id=None, email=None, phone=None):
        self.name = name
        self.uid = id
        self.email = email
        self.phone = phone

    def set_name(self, name):
        self.name = name

    def set_id(self, id):
        self.uid = id

    def set_email(self, email):
        self.email = email

    def set_phone(self, phone):
        self.phone = phone
    
    def set_account(self, account):
        self.account = account


class RItem():
    def __init__(self, item_name, item_price, idx=None, account = None):
        self.item_name = item_name
        self.item_price = item_price
        # self.item_proof = item_proof
        # self.claimant = Claimant(name, id, email, phone)
        if idx:
            self.item_idx = idx
        self.account = account
        # else:
        #     self.item_idx = self._create_idx()

    def set_idx(self, idx):
        self.item_idx = idx

    def __str__(self):
        return f"\033[94mReimbursement Item {self.item_idx}:\033[0m \t \033[4m{self.item_name}\033[0m \t \033[4m{self.item_price}\033[0m"
