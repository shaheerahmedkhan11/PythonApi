def add(num1: int, num2: int) -> int:
    return num1 + num2


def subtract(num1: int, num2: int) -> int:
    return num1 - num2


def multiply(num1: int, num2: int) -> int:
    return num1 * num2


def divide(num1: int, num2: int) -> float:
    if num2 == 0:
        raise ValueError("Cannot divide by zero.")
    return num1 / num2


class BankAccount:
    def __init__(self, starting_balance: float = 0.0):
        self.balance = starting_balance

    def deposit(self, amount: float) -> float:
        self.balance += amount

    def withdraw(self, amount: float) -> float:
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

    def get_balance(self) -> float:
        return self.balance

    def collect_interest(self) -> float:
        self.balance *= 1.1
