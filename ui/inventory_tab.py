from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
import sqlite3
import database
from database_manager import db_manager
from functools import partial


class InventoryTab(QWidget):
    def __init__(self, refresh_callback, edit_callback):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.edit_callback = edit_callback

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.load_data()

    def load_data(self):
        data = database.get_products()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(7)  # Removed ID column, now: Category, Name, Part Number, Description, Quantity, Edit, Delete
        self.table.setHorizontalHeaderLabels([
            "Category", "Name", "Part Number", "Description", "Quantity", "Edit", "Delete"
        ])
        
        for i, (id_, category, name, part_number, description, quantity) in enumerate(data):

            self.table.setItem(i, 0, QTableWidgetItem(category))
            self.table.setItem(i, 1, QTableWidgetItem(name))
            self.table.setItem(i, 2, QTableWidgetItem(part_number))
            self.table.setItem(i, 3, QTableWidgetItem(description))
            self.table.setItem(i, 4, QTableWidgetItem(str(quantity)))

            edit_button = QPushButton("✏️")
            edit_button.setToolTip("Edit this item")
            edit_button.setFixedSize(30, 30)
            edit_button.clicked.connect(partial(self.edit_callback, id_))

            edit_container = QWidget()
            edit_layout = QHBoxLayout()
            edit_layout.addWidget(edit_button)
            edit_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            edit_layout.setContentsMargins(0, 0, 0, 0)
            edit_container.setLayout(edit_layout)
            self.table.setCellWidget(i, 5, edit_container)

            delete_button = QPushButton("🗑️")
            delete_button.setToolTip("Delete this item")
            delete_button.setFixedSize(30, 30)
            delete_button.clicked.connect(partial(self.delete_row, id_))

            delete_container = QWidget()
            delete_layout = QHBoxLayout()
            delete_layout.addWidget(delete_button)
            delete_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            delete_layout.setContentsMargins(0, 0, 0, 0)
            delete_container.setLayout(delete_layout)
            self.table.setCellWidget(i, 6, delete_container)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.resizeColumnsToContents()

    def delete_row(self, product_id):
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete this product?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            database.delete_product(product_id)  # This should handle the DB logic
            self.load_data()
            self.refresh_callback()
