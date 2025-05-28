from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
import sqlite3
import database
from database import db_manager
from database import get_items_from_db

class AssetCategoryTab(QWidget):
    def __init__(self, refresh_callback, edit_callback, category=None):
        super().__init__()
        self.category = category
        self.refresh_callback = refresh_callback
        self.edit_callback = edit_callback
        self.category = category
        self.setup_ui()
        self.load_data()

    def load_data(self):
        from database import get_items_from_db
        items = get_items_from_db(self.category)
        self.table.setRowCount(len(items))
        
        for i, (id_, category, name, part_number, description, quantity) in enumerate(items):
            self.table.setItem(i, 0, QTableWidgetItem(category))
            self.table.setItem(i, 1, QTableWidgetItem(name))
            self.table.setItem(i, 2, QTableWidgetItem(part_number))
            self.table.setItem(i, 3, QTableWidgetItem(description))
            qty_item = QTableWidgetItem(str(quantity))
            if quantity < 1:
                qty_item.setBackground(Qt.GlobalColor.red)
            self.table.setItem(i, 4, qty_item)

            edit_button = QPushButton("✏️")
            edit_button.setToolTip("Edit this item")
            edit_button.setFixedSize(30, 30)
            edit_button.clicked.connect(lambda _, row_id=id_: self.edit_callback(row_id))

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
            delete_button.clicked.connect(lambda _, row_id=id_: self.delete_row(row_id))

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
            f"Are you sure you want to delete this item?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect(db_manager.current_db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            conn.close()
            self.load_data()
            self.refresh_callback()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Category", "Name", "Part Number", "Description", "Quantity", "Edit", "Delete"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Optional: make table read-only

        layout.addWidget(self.table)
        self.setLayout(layout)