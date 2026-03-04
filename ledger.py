"""
AccountLedger (intentionally flawed scaffold)

Informal requirement (deliberately vague; see requirement.md from last week):
- Maintain account balances.
- Allow deposits, withdrawals, and transfers.
- Record transactions so the system is auditable.

This week's focus (Test Data Selection as Risk Management):
- The implementation contains several "risk regions" where behavior changes:
  - boundary conditions (e.g., withdrawing an amount equal to the balance)
  - invalid inputs (negative/zero amounts)
  - messy identifiers ("A" vs "A " vs " a ")
  - silent account creation
  - conservation / accounting consistency across transfers

The code is intentionally imperfect. The goal is NOT to redesign it, but to
reason about test data: what inputs are currently exercised, what are missing,
and which small set of additional tests would meaningfully reduce risk.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
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
    - Account IDs are inconsistently normalized (e.g., "A" vs "A ").
    - Unknown accounts are sometimes treated as 0.0, sometimes created silently.
    - Amount validation is weak and inconsistent across operations.
    - Withdrawals use an incorrect boundary check (>=) that rejects withdrawing
      the full balance. (A classic boundary bug.)
    - Transfers apply a fee incorrectly (only debited, not credited), breaking
      conservation in non-obvious ways.
    - No explicit invariant enforcement (e.g., non-negative balances) beyond a
      few partial checks.
    - Returns are inconsistent (some methods return bool, others raise).
    - transactions() exposes internal list directly.

    NOTE: These are intentional. This week's lab is about choosing test data
    that discovers these issues, especially around boundaries and invalid inputs.
    """

    def __init__(self) -> None:
        self._balances: Dict[str, float] = {}
        self._txns: List[Txn] = []

    # -----------------------------
    # Internal helpers (intentionally imperfect)
    # -----------------------------
    def _normalize_id(self, account_id: str) -> str:
        """
        Intentionally flawed normalization.

        - We strip outer whitespace (reasonable).
        - We DO NOT enforce case consistency (so "A" and "a" remain distinct).
        - We allow empty IDs after stripping (bad).
        """
        return str(account_id).strip()

    def _ensure_account(self, account_id: str) -> str:
        """
        Intentionally permissive:
        - creates accounts on-the-fly with 0.0 balance.
        """
        aid = self._normalize_id(account_id)
        if aid not in self._balances:
            self._balances[aid] = 0.0
            # Record a "create" implicitly (also questionable behavior).
            self._record(
                kind="create",
                source=None,
                target=aid,
                amount=0.0,
                meta={"implicit": True},
            )
        return aid

    # -----------------------------
    # Public API
    # -----------------------------
    def create_account(self, account_id: str, initial_balance: float = 0.0) -> None:
        # Intentionally permissive: overwrites silently.
        aid = self._normalize_id(account_id)
        self._balances[aid] = float(initial_balance)
        self._record(
            kind="create",
            source=None,
            target=aid,
            amount=float(initial_balance),
            meta={"implicit": False},
        )

    def balance(self, account_id: str) -> float:
        # Intentionally permissive: unknown account treated as 0.0 (no error).
        aid = self._normalize_id(account_id)
        return float(self._balances.get(aid, 0.0))

    def deposit(self, account_id: str, amount: float) -> None:
        """
        Deposit funds.

        Intentional flaws:
        - silently creates account.
        - accepts amount == 0 (pointless) and negative amounts (acts like withdrawal).
        - no rounding policy for cents.
        """
        aid = self._ensure_account(account_id)
        amt = float(amount)
        self._balances[aid] += amt
        self._record(kind="deposit", source=None, target=aid, amount=amt, meta={})

    def withdraw(self, account_id: str, amount: float) -> bool:
        """
        Withdraw funds.

        Intentional flaws:
        - silently creates account.
        - rejects withdrawing the *full* balance due to >= boundary bug.
        - accepts negative withdrawals (acts like deposit).
        - returns bool (rather than raising) and uses inconsistent failure mode.
        """
        aid = self._ensure_account(account_id)
        amt = float(amount)

        # Inconsistent: treat non-positive as "invalid" but just return False.
        if amt <= 0:
            self._record(
                kind="withdraw",
                source=aid,
                target=None,
                amount=amt,
                meta={"result": "invalid"},
            )
            return False

        # Intentional boundary bug: should be (amt > balance), but uses >=
        if amt >= self._balances[aid]:
            self._record(
                kind="withdraw",
                source=aid,
                target=None,
                amount=amt,
                meta={"result": "declined"},
            )
            return False

        self._balances[aid] -= amt
        self._record(
            kind="withdraw", source=aid, target=None, amount=amt, meta={"result": "ok"}
        )
        return True

    def transfer(self, source: str, target: str, amount: float) -> bool:
        """
        Transfer amount from source to target.

        Intentional flaws:
        - silently creates missing accounts for both source and target.
        - allows self-transfer (source == target) with surprising behavior.
        - fee applied only to debit side, breaking conservation.
        - insufficient-funds handling is inconsistent: returns False vs raising.
        - accepts amount <= 0 as "invalid" but returns False (no exception).
        """
        src = self._ensure_account(source)
        tgt = self._ensure_account(target)
        amt = float(amount)

        if amt <= 0:
            self._record(
                kind="transfer",
                source=src,
                target=tgt,
                amount=amt,
                meta={"result": "invalid"},
            )
            return False

        # Subtle boundary decision (and still imperfect): allow draining to zero.
        if amt > self._balances[src]:
            self._record(
                kind="transfer",
                source=src,
                target=tgt,
                amount=amt,
                meta={"result": "insufficient_funds"},
            )
            return False

        # Intentional accounting bug: fee applied only to debit side.
        fee = 0.50 if amt >= 1000 else 0.0

        self._balances[src] -= amt + fee
        self._balances[tgt] += amt

        self._record(
            kind="transfer",
            source=src,
            target=tgt,
            amount=amt,
            meta={"fee": fee, "result": "ok"},
        )
        return True

    def transactions(self) -> List[Txn]:
        # Exposes internal list directly (intentional).
        return self._txns

    # -----------------------------
    # Recording
    # -----------------------------
    def _record(
        self,
        kind: str,
        source: Optional[str],
        target: Optional[str],
        amount: float,
        meta: dict,
    ) -> None:
        txn = Txn(
            id=str(uuid.uuid4()),
            # Slightly improved timestamp policy (timezone-aware), but still string.
            ts=datetime.now(timezone.utc).isoformat(),
            kind=kind,
            source=source,
            target=target,
            amount=float(amount),
            meta=dict(meta),
        )
        self._txns.append(txn)


if __name__ == "__main__":
    # Minimal smoke demo (not a test suite).
    l = AccountLedger()
    l.create_account("Alice", 100.0)
    l.create_account("Bob", 25.0)
    l.deposit("Alice", 10.0)
    ok = l.withdraw("Alice", 50.0)
    print("withdraw ok?", ok, "Alice balance:", l.balance("Alice"))
    ok = l.transfer("Alice", "Bob", 40.0)
    print("transfer ok?", ok, "Alice:", l.balance("Alice"), "Bob:", l.balance("Bob"))
    print("txns:", len(l.transactions()))
