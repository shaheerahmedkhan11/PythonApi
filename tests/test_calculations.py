from app.calculations import add, subtract, multiply, divide, BankAccount
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount(100)

@pytest.mark.parametrize(
    "num1, num2, expected", [(2, 3, 5), (-1, 1, 0), (0, 0, 0), (-2, -3, -5)]
)
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0
    assert subtract(-1, -1) == 0
    assert subtract(-5, -3) == -2


def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 1) == -1
    assert multiply(0, 5) == 0
    assert multiply(-2, -3) == 6


def test_divide():
    assert divide(6, 3) == 2.0
    assert divide(-6, 2) == -3.0
    assert divide(5, 2) == 2.5
    try:
        divide(5, 0)
    except ValueError as e:
        assert str(e) == "Cannot divide by zero."

def test_bank_account(zero_bank_account):
    assert zero_bank_account.get_balance() == 100.0

def test_deposit(zero_bank_account):
    zero_bank_account.deposit(25)
    assert zero_bank_account.get_balance() == 125.0

def test_withdraw(zero_bank_account):
    zero_bank_account.withdraw(40)
    assert zero_bank_account.get_balance() == 60.0
    try:
        zero_bank_account.withdraw(100)
    except ValueError as e:
        assert str(e) == "Insufficient funds."

@pytest.mark.parametrize(
    "starting_balance, expected_balance",[
        (100, 110),
        (200, 220),
    ])
def test_collect_interest(zero_bank_account, starting_balance, expected_balance):
    zero_bank_account = BankAccount(starting_balance)
    zero_bank_account.collect_interest()
    assert round(zero_bank_account.get_balance()) == expected_balance 