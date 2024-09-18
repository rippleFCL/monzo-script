import logging
import time
from datetime import datetime
from uuid import uuid4

from monzo.authentication import Authentication
from monzo.endpoints.account import Account
from monzo.endpoints.pot import Pot
from monzo.endpoints.transaction import Transaction

logger = logging.getLogger(__name__)


class MonzoPot(object):
    def __init__(self, pot: Pot):
        self.pot = pot

    @classmethod
    def from_pots(cls, pots: list[Pot]) -> "list[MonzoPot]":
        return [cls.from_pot(pot) for pot in pots]

    @classmethod
    def from_pot(cls, pot: Pot) -> "MonzoPot":
        return cls(pot)

    def update(self, pot: Pot) -> None:
        self.pot = pot
