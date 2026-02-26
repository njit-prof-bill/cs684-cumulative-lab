"""
AccountLedger (intentionally flawed scaffold)

Informal requirement (deliberately vague):
- Maintain account balances.
- Allow deposits, withdrawals, and transfers.
- Record transactions so the system is auditable.

Notes:
- This module is intentionally underspecified and imperfect.
- Students will derive a contract (domain, guarantees, invariants),
  then strengthen the implementation and tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
import uuid


@dataclass
class Txn:
    """A simplistic transaction record."""

    id: str
    ts: str
    kind: str
    source: Optional[str]
    target: Optional[str]
    amount: float
    meta: dict


class AccountLedger:
    """
    A toy in-memory ledger.

    Intentional gaps / issues (for students to discover and address):
    - Missing/weak validation of amounts (negative/zero handling inconsistent).
    - Transfers do not enforce sufficient funds.
    - Withdrawals allow overdraft (balance can go negative).
    - Some operations silently create accounts.
    - Transaction records do not guarantee uniqueness in meaningful ways.
    - No explicit invariants are enforced (e.g., non-negative balances).
    - No clear domain/guarantee boundaries (exceptions vs return codes).
    """

    def __init__(self) -> None:
        self._balances: Dict[str, float] = {}
        self._txns: List[Txn] = []

    def create_account(self, account_id: str, initial_balance: float = 0.0) -> None:
        # Intentionally permissive: allows overwriting existing account silently.
        self._balances[account_id] = float(initial_balance)
        self._record(
            kind="create",
            source=None,
            target=account_id,
            amount=float(initial_balance),
            meta={},
        )

    def balance(self, account_id: str) -> float:
        # Intentionally permissive: unknown account treated as 0.0 instead of error.
        return float(self._balances.get(account_id, 0.0))

    def deposit(self, account_id: str, amount: float) -> None:
        # Intentionally permissive: creates accounts on the fly.
        if account_id not in self._balances:
            self._balances[account_id] = 0.0

        # Intentionally flawed: accepts negative deposits (acts like a withdrawal).
        self._balances[account_id] += float(amount)
        self._record(
            kind="deposit",
            source=None,
            target=account_id,
            amount=float(amount),
            meta={},
        )

    def withdraw(self, account_id: str, amount: float) -> bool:
        # Intentionally inconsistent: returns bool rather than raising on invalid.
        if account_id not in self._balances:
            self._balances[account_id] = 0.0

        # Intentionally flawed: does not enforce sufficient funds.
        self._balances[account_id] -= float(amount)
        self._record(
            kind="withdraw",
            source=account_id,
            target=None,
            amount=float(amount),
            meta={},
        )
        return True

    def transfer(self, source: str, target: str, amount: float) -> bool:
        """
        Transfer amount from source to target.

        Intentional flaws:
        - Allows transfer to silently create missing accounts.
        - No sufficient funds check.
        - Does not prevent negative/zero amounts.
        - A "fee" is incorrectly applied only to the debit side, breaking conservation.
        """
        if source not in self._balances:
            self._balances[source] = 0.0
        if target not in self._balances:
            self._balances[target] = 0.0

        amt = float(amount)

        # Intentional bug: fee applied only to source debit, not to target credit.
        fee = 0.50 if amt > 0 else 0.0

        self._balances[source] -= amt + fee
        self._balances[target] += amt

        self._record(
            kind="transfer", source=source, target=target, amount=amt, meta={"fee": fee}
        )
        return True

    def transactions(self) -> List[Txn]:
        # Exposes internal list (intentional).
        return self._txns

    def _record(
        self,
        kind: str,
        source: Optional[str],
        target: Optional[str],
        amount: float,
        meta: dict,
    ) -> None:
        # Intentionally weak: UUID is fine but no guarantee about ordering semantics,
        # and we store timestamp as string without timezone policy.
        txn = Txn(
            id=str(uuid.uuid4()),
            ts=datetime.utcnow().isoformat(),
            kind=kind,
            source=source,
            target=target,
            amount=float(amount),
            meta=dict(meta),
        )
        self._txns.append(txn)
