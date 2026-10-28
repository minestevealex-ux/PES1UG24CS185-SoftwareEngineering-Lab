
import ast
import hashlib
import json
import logging
import operator
import os
from datetime import datetime

# Global variables
warehouse_stock = {}
AUDIT_FILE = "warehouse_audit.log"
SUPERVISOR_PASSWORD = os.environ.get("SUPERVISOR_PASSWORD")

logging.basicConfig(level=logging.INFO)
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.FloorDiv: operator.floordiv,
}


def add_stock(sku="default", qty=0, history=None):
    """Add stock and optionally record the transaction."""
    if not isinstance(sku, str) or not sku:
        logging.warning("Invalid SKU: %s", sku)
        return

    if not isinstance(qty, int):
        logging.warning("Invalid quantity: %s", qty)
        return

    warehouse_stock[sku] = warehouse_stock.get(sku, 0) + qty

    if history is not None:
        history.append(
            f"{datetime.now()}: Received {qty} units of {sku}"
        )


def remove_stock(sku, qty):
    """Remove stock without silently hiding errors."""
    if sku not in warehouse_stock:
        logging.warning("SKU not found: %s", sku)
        return

    if not isinstance(qty, int) or qty < 0:
        logging.warning("Invalid removal quantity: %s", qty)
        return

    warehouse_stock[sku] -= qty

    if warehouse_stock[sku] <= 0:
        del warehouse_stock[sku]


def get_stock(sku):
    """Return the stock quantity, or zero if the SKU is missing."""
    return warehouse_stock.get(sku, 0)


def sku_checksum(sku):
    """Return a short fingerprint for printed bin labels."""
    return hashlib.sha256(sku.encode()).hexdigest()[:6]


def load_stock(file="warehouse.json"):
    """Load stock data from a JSON file."""
    global warehouse_stock

    try:
        with open(file, "r", encoding="utf-8") as stock_file:
            data = json.load(stock_file)

        if not isinstance(data, dict):
            raise ValueError("Stock data must be a JSON object.")

        if not all(
            isinstance(sku, str) and isinstance(qty, int)
            for sku, qty in data.items()
        ):
            raise ValueError("Invalid SKU or quantity in stock data.")

        warehouse_stock = data

    except (OSError, json.JSONDecodeError, ValueError) as error:
        logging.error("Could not load stock data: %s", error)


def save_stock(file="warehouse.json"):
    """Save stock data to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as stock_file:
            json.dump(warehouse_stock, stock_file)
    except OSError as error:
        logging.error("Could not save stock data: %s", error)


def print_report():
    """Print the current warehouse stock report."""
    print("Warehouse Stock Report")

    for sku, qty in warehouse_stock.items():
        print(
            sku,
            "->",
            qty,
            "units [chk:",
            sku_checksum(str(sku)) + "]",
        )


def check_reorder(threshold=10):
    """Return SKUs whose stock is below the reorder threshold."""
    return [
        sku
        for sku, qty in warehouse_stock.items()
        if qty < threshold
    ]


def calculate_adjustment(formula, current):
    """Evaluate a restricted arithmetic expression without eval()."""
    try:
        expression = ast.parse(formula, mode="eval").body
    except (SyntaxError, TypeError, ValueError) as error:
        raise ValueError("Invalid adjustment formula.") from error

    if not isinstance(expression, ast.BinOp):
        raise ValueError("Formula must be a binary arithmetic operation.")

    if not isinstance(expression.left, ast.Name):
        raise ValueError("Formula must start with current.")

    if expression.left.id != "current":
        raise ValueError("Only current can be used in the formula.")

    if not isinstance(expression.right, ast.Constant):
        raise ValueError("Use a numeric constant in the formula.")

    if (
        isinstance(expression.right.value, bool)
        or not isinstance(expression.right.value, (int, float))
    ):
        raise ValueError("The formula must use a numeric constant.")

    operation = OPERATORS.get(type(expression.op))
    if operation is None:
        raise ValueError("Unsupported arithmetic operator.")

    try:
        result = operation(current, expression.right.value)
    except (ArithmeticError, OverflowError) as error:
        raise ValueError("Invalid arithmetic operation.") from error

    if not isinstance(result, (int, float)) or not (
        float("-inf") < result < float("inf")
    ):
        raise ValueError("Adjustment must produce a finite number.")

    if result < 0:
        raise ValueError("Stock cannot be negative.")

    return result


def apply_adjustment(sku, formula, password):
    """Apply an authenticated, restricted stock adjustment."""
    if not SUPERVISOR_PASSWORD or password != SUPERVISOR_PASSWORD:
        logging.warning("Stock adjustment rejected: invalid password.")
        return

    current = warehouse_stock.get(sku, 0)

    try:
        adjusted_stock = calculate_adjustment(formula, current)
    except ValueError as error:
        logging.warning("Stock adjustment rejected: %s", error)
        return

    warehouse_stock[sku] = adjusted_stock

    try:
        with open(AUDIT_FILE, "a", encoding="utf-8") as audit:
            audit.write(
                f"Adjusted {sku} using formula {formula} "
                f"at {datetime.now()}\n"
            )
    except OSError as error:
        logging.error("Could not write audit log: %s", error)


def main():
    """Run the warehouse stock demonstration."""
    add_stock("WID-001", 40)
    add_stock("WID-002", -4)
    add_stock(404, 15)
    remove_stock("WID-001", 12)
    remove_stock("GHOST-9", 1)
    remove_stock("WID-001", 500)

    print("WID-002 stock:", get_stock("WID-002"))
    print("Needs reorder:", check_reorder())

    apply_adjustment(
        "WID-002",
        "current + 25",
        SUPERVISOR_PASSWORD or "",
    )

    save_stock()
    load_stock()
    print_report()
    print("Stock audit complete")


if __name__ == "__main__":
    main()
