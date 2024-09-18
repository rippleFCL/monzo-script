import logging
import os
import sys
import time

from monzo_optimiser import AuthedApi, MonzoManager

# from account_processor import (
#     AccountManager,
#     PotGoalProcessor,
#     PotMinimumProcessor,
#     RoundupProcessor,
#     SavingsOverflowProcessor,
#     SavingsPercentageProcessor,
# )

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)



CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URL"]


authed_api = AuthedApi.from_file("./.creds", CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
monzo_account = MonzoManager.new(authed_api)
monzo_account.update()


# account_managers: list[AccountManager] = []
# for account in accounts:
#     if account.account_type() != "UNKNOWN":
#         logger.info("acctype: %s, accid: %s", account.account_type(), account.account_id)
#         pot_manager = MonzoManager.from_account(auth, account)
#         account_manager = AccountManager(auth, account, pot_manager, dry_run=False)
#         account_manager.register_processor(PotMinimumProcessor(pot_manager))
#         account_manager.register_processor(SavingsPercentageProcessor(pot_manager))
#         account_manager.register_processor(PotGoalProcessor(pot_manager))
#         account_manager.register_processor(SavingsOverflowProcessor(pot_manager))
#         account_manager.register_processor(RoundupProcessor(pot_manager))
#         account_managers.append(account_manager)

# while 1:
#     time.sleep(2)
#     for account_manager in account_managers:
#         logger.debug(f"optimizing account {account_manager}")
#         account_manager.optimize_account()
