import json

# Inventory file to store grocery data
INVENTORY_FILE = 'grocery_inventory.json'


class Grocery:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity


class GroceryManagement:
    def __init__(self):
        self.inventory = self.load_inventory()

    def load_inventory(self):
        try:
            with open(INVENTORY_FILE, 'r') as file:
                inventory = json.load(file)
                return [Grocery(item['name'], item['price'], item['quantity']) for item in inventory]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_inventory(self):
        with open(INVENTORY_FILE, 'w') as file:
            json.dump([{'name': item.name, 'price': item.price, 'quantity': item.quantity} for item in self.inventory], file)

    def add_item(self, name, price, quantity):
        new_item = Grocery(name, price, quantity)
        self.inventory.append(new_item)
        self.save_inventory()
        print(f"Item '{name}' added successfully.")

    def display_inventory(self):
        print("\n--- Grocery Inventory ---")
        for idx, item in enumerate(self.inventory, 1):
            print(f"{idx}. Name: {item.name}, Price: {item.price}, Quantity: {item.quantity}")
        print("\n")

    def search_item(self, name):
        for item in self.inventory:
            if item.name.lower() == name.lower():
                print(f"Item found - Name: {item.name}, Price: {item.price}, Quantity: {item.quantity}")
                return item
        print("Item not found.")
        return None

    def update_item(self, name, price=None, quantity=None):
        item = self.search_item(name)
        if item:
            if price is not None:
                item.price = price
            if quantity is not None:
                item.quantity = quantity
            self.save_inventory()
            print(f"Item '{name}' updated successfully.")

    def delete_item(self, name):
        item = self.search_item(name)
        if item:
            self.inventory.remove(item)
            self.save_inventory()
            print(f"Item '{name}' deleted successfully.")

    def generate_bill(self, purchase_list):
        total = 0
        for item_name, quantity in purchase_list:
            item = self.search_item(item_name)
            if item and item.quantity >= quantity:
                total += item.price * quantity
                item.quantity -= quantity
                self.save_inventory()
            else:
                print(f"Insufficient stock for item '{item_name}' or item not found.")
        print(f"\nTotal Bill: ${total:.2f}")


def main():
    system = GroceryManagement()

    while True:
        print("\n--- Grocery Management System ---")
        print("1. Add Grocery Item")
        print("2. View Inventory")
        print("3. Search Item")
        print("4. Update Item")
        print("5. Delete Item")
        print("6. Generate Bill")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            quantity = int(input("Enter item quantity: "))
            system.add_item(name, price, quantity)

        elif choice == '2':
            system.display_inventory()

        elif choice == '3':
            name = input("Enter item name to search: ")
            system.search_item(name)

        elif choice == '4':
            name = input("Enter item name to update: ")
            price = input("Enter new price (or leave blank to keep current): ")
            quantity = input("Enter new quantity (or leave blank to keep current): ")
            price = float(price) if price else None
            quantity = int(quantity) if quantity else None
            system.update_item(name, price, quantity)

        elif choice == '5':
            name = input("Enter item name to delete: ")
            system.delete_item(name)

        elif choice == '6':
            purchase_list = []
            while True:
                item_name = input("Enter item name to purchase (or 'done' to finish): ")
                if item_name.lower() == 'done':
                    break
                quantity = int(input("Enter quantity: "))
                purchase_list.append((item_name, quantity))
            system.generate_bill(purchase_list)

        elif choice == '7':
            print("Exiting system.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
