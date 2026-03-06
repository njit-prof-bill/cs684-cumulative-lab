
"""
Weak tests (intentional)

These tests are not "wrong" syntactically, but they are not good tests.
They allow major defects to survive (negative balances, conservation violations, etc.)

Students will:
- derive a real contract from intent
- strengthen assertions (oracles)
- add invariant checks
- add negative/edge case tests
- run their test suite
"""

from ledger import AccountLedger


def test_create_account_and_balance_round_trip():
    l = AccountLedger()
    l.create_account("alice", 100.0)
    assert l.balance("alice") == 100.0


def test_deposit_increases_balance():
    l = AccountLedger()
    l.create_account("alice", 0.0)
    l.deposit("alice", 25.0)
    assert l.balance("alice") == 25.0


def test_transfer_moves_money_somehow():
    l = AccountLedger()
    l.create_account("alice", 100.0)
    l.create_account("bob", 0.0)

    ok = l.transfer("alice", "bob", 10.0)
    assert ok is True

    # Weak assertions: only checks that *something* changed in the expected direction.
    assert l.balance("bob") > 0.0
    assert l.balance("alice") < 100.0


def test_transactions_are_recorded():
    l = AccountLedger()
    l.create_account("alice", 5.0)
    l.deposit("alice", 1.0)
    assert len(l.transactions()) >= 2
