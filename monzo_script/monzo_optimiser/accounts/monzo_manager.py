from monzo_optimiser.authed_api import AuthedApi
from monzo_optimiser.pots.monzo_pots import MonzoPot
from monzo_optimiser.accounts.account_manager import AccountManager
# from monzo.authentication import Authentication
from monzo.endpoints.account import Account
from monzo.endpoints.pot import Pot

class MonzoManager(object):
    def __init__(self, authed_api: AuthedApi, accounts: dict[str, AccountManager]):
        self.accounts = accounts
        self.authed_api = authed_api

    @classmethod
    def new(cls, authed_api: AuthedApi) -> "MonzoManager":
        monzo_accounts = authed_api.fetch_accounts()
        accounts = {}
        for account in monzo_accounts:
            pots =  authed_api.fetch_pots(account)
            account_manager = cls._create_account_manager(account, pots)
            accounts[account.account_id] = account_manager
        return cls(authed_api, accounts)

    @staticmethod
    def _create_account_manager(account: Account, pots: list[Pot]) -> AccountManager:
        return AccountManager.from_pots(account, pots)

    def update(self) -> None:
        monzo_accounts = self.authed_api.fetch_accounts()
        for account in monzo_accounts:
            pots =  self.authed_api.fetch_pots(account)
            if account.account_id not in self.accounts:
                account_manager = AccountManager.from_pots(account, pots)
                self.accounts[account.account_id] = account_manager
            else:
                self.accounts[account.account_id].update(account, pots)

        account_ids = [account.account_id for account in monzo_accounts]

        for account_id in list(self.accounts): # exhaust the iterator or the keys before working on the dictionary
            if account_id not in account_ids:
                del self.accounts[account_id]

