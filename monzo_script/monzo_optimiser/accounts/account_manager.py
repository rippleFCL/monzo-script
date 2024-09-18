import stat
from monzo.endpoints.account import Account
from monzo.endpoints.pot import Pot
from monzo_optimiser.pots.monzo_pots import MonzoPot
from monzo_optimiser.pots.pot_procsessors import AccountProcessorInterface,
# from monzo_optimiser.transactions.transaction_controllers import AccountTransactionGroup, AccountTransactionGroupInterface


class AccountManager:
    def __init__(self, account: Account, pots: dict[str, MonzoPot], account_processors: list[AccountProcessorInterface]) -> None:
        self.account_processors:  = []
        self.account = account
        self.pots = pots

    @classmethod
    def from_pots(cls, account: Account, pots: list[Pot]) -> "AccountManager":
        pot_dict = {pot.pot_id: MonzoPot.from_pot(pot) for pot in pots}
        return cls(account, pot_dict, cls._create_account_processors())

    @staticmethod
    def _create_account_processors() -> list[AccountProcessorInterface]:
        return []

    @staticmethod
    def _create_pot(pots: Pot) -> MonzoPot:
        return MonzoPot.from_pot(pots)

    def update(self, account: Account, pots: list[Pot]) -> None:
        self.account = account
        for pot in pots:
            if pot.pot_id in self.pots:
                self.pots[pot.pot_id].update(pot)
            else:
                self.pots[pot.pot_id] = self._create_pot(pot)

        pot_ids = [pot.pot_id for pot in pots]
        for pot_id in list(self.pots):
            if pot_id not in pot_ids:
                del self.pots[pot_id]

    # def _make_transaction_group(self) -> AccountTransactionGroupInterface:
    #     return AccountTransactionGroup.from_account(self.auth, self.account, self.pot_manager)

    # def register_processor(self, processor: AccountProcessorInterface) -> None:
    #     self.account_processors.append(processor)

    # def optimize_account(self) -> None:
    #     transaction_controller = self._make_transaction_group()
    #     for account_processor in self.account_processors:
    #         account_processor.process(transaction_controller)
    #     transaction_controller.execute(self.dry_run)
    #     self.pot_manager.update()
