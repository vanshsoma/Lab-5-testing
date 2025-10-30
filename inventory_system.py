"""
A simple file-based inventory management system.

This module allows adding, removing, and querying item quantities,
and persists the inventory data to a JSON file.
"""

import json
import logging

# Global variable to hold inventory state
stock_data = {}


def add_item(item="default", qty=0):
    """
    Add a specified quantity of an item to the inventory.

    Args:
        item (str): The name of the item to add.
        qty (int): The quantity to add. Must be a positive integer.
    """
    # Input validation
    if not isinstance(item, str) or not item:
        logging.error("Invalid item name: %s. Must be a non-empty string.", item)
        return
    if not isinstance(qty, int):
        logging.error("Invalid quantity: %s. Must be an integer.", qty)
        return
    if qty <= 0:
        logging.warning("Quantity must be positive. Received: %s. Not adding.", qty)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logging.info("Added %s of %s. New total: %s.", qty, item, stock_data[item])


def remove_item(item, qty):
    """
    Remove a specified quantity of an item from the inventory.

    If the quantity drops to 0 or below, the item is removed.

    Args:
        item (str): The name of the item to remove.
        qty (int): The quantity to remove. Must be a positive integer.
    """
    # Input validation
    if not isinstance(item, str) or not item:
        logging.error("Invalid item name: %s. Must be a non-empty string.", item)
        return
    if not isinstance(qty, int) or qty <= 0:
        logging.error("Invalid quantity: %s. Must be a positive integer.", qty)
        return

    try:
        if stock_data[item] <= qty:
            del stock_data[item]
            logging.info("Removed item '%s' from stock (was %s or less).",
                         item, qty)
        else:
            stock_data[item] -= qty
            logging.info("Removed %s of %s. New total: %s.",
                         qty, item, stock_data[item])
    except KeyError:
        # Specific exception! Fixes B110, W0702, E722
        logging.warning("Item '%s' not in stock, cannot remove.", item)
    except TypeError:
        # Added for robustness in case data is corrupted
        logging.error("Data for item '%s' is corrupt. Could not remove.", item)


def get_qty(item):
    """
    Get the current quantity of a specific item.

    Args:
        item (str): The name of the item to query.

    Returns:
        int: The quantity in stock, or 0 if the item is not found.
    """
    if not isinstance(item, str):
        logging.error("Invalid item name: %s. Must be a string.", item)
        return 0
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Load the inventory data from a JSON file into the global stock_data.
    This modifies the global 'stock_data' dictionary in place.

    Args:
        file (str): The name of the file to load from.
    """
    try:
        # Use 'with' and specify encoding. Fixes R1732, W1514
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Modify global in place to avoid 'global' statement. Fixes W0603
        stock_data.clear()
        stock_data.update(data)
        logging.info("Inventory loaded successfully from %s.", file)
    except FileNotFoundError:
        logging.warning("Inventory file '%s' not found. Starting fresh.", file)
    except json.JSONDecodeError:
        logging.error("Could not decode JSON from '%s'. Starting fresh.", file)


def save_data(file="inventory.json"):
    """
    Save the current inventory data to a JSON file.

    Args:
        file (str): The name of the file to save to.
    """
    try:
        # Use 'with' and specify encoding. Fixes R1732, W1514
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
        logging.info("Inventory saved successfully to %s.", file)
    except IOError as e:
        logging.error("Could not save inventory to %s: %s", file, e)


def print_data():
    """Print a formatted report of all items in stock."""
    print("\n--- Items Report ---")
    if not stock_data:
        print("  Inventory is empty.")
    for item, qty in stock_data.items():
        print(f"  {item}: {qty}")  # f-string is fine here, it's not logging
    print("----------------------\n")


def check_low_items(threshold=5):
    """
    Find all items at or below a given stock threshold.

    Args:
        threshold (int): The stock level to check against.

    Returns:
        list: A list of item names that are low in stock.
    """
    return [item for item, qty in stock_data.items() if qty <= threshold]


def main():
    """
    Main function to run the inventory system demo.
    """
    # Configure logging. Fixes W0611, F401 (unused import)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    load_data("inventory.json")

    add_item("apple", 10)
    add_item("banana", 25)

    # These invalid calls will now be gracefully handled and logged
    add_item("banana", -2)  # Invalid quantity
    add_item(123, "ten")    # Invalid types

    remove_item("apple", 3)
    remove_item("orange", 1)  # Will log a warning (item not in stock)

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")

    print_data()
    save_data("inventory.json")

    # Removed the 'eval()' line. Fixes B307, W0123


if __name__ == "__main__":
    main()
