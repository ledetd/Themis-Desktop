import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from database_manager import db_manager  # Assuming db_manager is handling the connection

class EditItemsTab(QWidget):
    def __init__(self, refresh_callback):
        super().__init__()
        self.refresh_callback = refresh_callback
        layout = QVBoxLayout()

        # Initialize the table to show products
        self.table = QTableWidget()
        self.table.setColumnCount(5)  # Without ID column
        self.table.setHorizontalHeaderLabels(["Category", "Name", "Part Number", "Description", "Quantity"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers)
        layout.addWidget(self.table)

        # Button to save changes
        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.load_data()

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.resizeColumnsToContents()

    def load_data(self):
        try:
            # Using db_manager to get the connection
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            conn.close()

            # Load the data into the table
            self.table.setRowCount(len(rows))
            for i, (id_, category, name, part_number, description, quantity) in enumerate(rows):
                # Store the product ID in the category cell's user role (hidden)
                cat_item = QTableWidgetItem(category)
                cat_item.setData(Qt.ItemDataRole.UserRole, id_)
                self.table.setItem(i, 0, cat_item)

                self.table.setItem(i, 1, QTableWidgetItem(name))
                self.table.setItem(i, 2, QTableWidgetItem(part_number))
                self.table.setItem(i, 3, QTableWidgetItem(description))
                self.table.setItem(i, 4, QTableWidgetItem(str(quantity)))
        except sqlite3.DatabaseError as e:
            print(f"Error loading data: {e}")
            QMessageBox.critical(self, "Database Error", "Failed to load data from the database.")

    def save_changes(self):
        try:
            conn = db_manager.get_connection()
            cursor = conn.cursor()

            # Begin transaction for better performance
            cursor.execute("BEGIN TRANSACTION;")
            
            for row in range(self.table.rowCount()):
                # Retrieve product ID from hidden data stored in category cell
                cat_item = self.table.item(row, 0)
                if cat_item is None:
                    continue
                item_id = cat_item.data(Qt.ItemDataRole.UserRole)

                # Get the new values from the table
                category = cat_item.text().strip()
                name_item = self.table.item(row, 1)
                part_number_item = self.table.item(row, 2)
                description_item = self.table.item(row, 3)
                quantity_item = self.table.item(row, 4)

                if None in (name_item, part_number_item, description_item, quantity_item):
                    continue

                name = name_item.text().strip()
                part_number = part_number_item.text().strip()
                description = description_item.text().strip()

                # Validate and convert quantity
                quantity_text = quantity_item.text().strip()
                try:
                    quantity = int(quantity_text) if quantity_text else 0
                except ValueError:
                    QMessageBox.warning(self, "Invalid Input", f"Invalid quantity at row {row + 1}. Please enter a valid number.")
                    continue

                # Update the product in the database
                cursor.execute("""
                    UPDATE products
                    SET category = ?, name = ?, part_number = ?, description = ?, quantity = ?
                    WHERE id = ?
                """, (category, name, part_number, description, quantity, item_id))

            # Commit the transaction
            cursor.execute("COMMIT;")
            conn.close()

            # Refresh UI and notify the user
            self.refresh_callback()
            QMessageBox.information(self, "Saved", "Changes saved successfully.")

        except sqlite3.DatabaseError as e:
            print(f"Error saving changes: {e}")
            QMessageBox.critical(self, "Database Error", "Failed to save changes to the database.")
