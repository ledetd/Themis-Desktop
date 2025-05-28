import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QToolBar, QPushButton, QComboBox, QInputDialog, QMessageBox
)

from database import init_db
from database_manager import db_manager
from ui.inventory_tab import InventoryTab
from ui.add_product_tab import AddProductTab
from ui.edit_items_tab import EditItemsTab
from ui.asset_tab import AssetTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Themis - Inventory Manager")
        self.setMinimumSize(800, 700)

        # === Toolbar ===
        self.project_selector = QComboBox()
        self.load_existing_projects()
        self.project_selector.currentTextChanged.connect(self.switch_project)

        toolbar = QToolBar("Projects")
        toolbar.addWidget(self.project_selector)

        new_project_btn = QPushButton("➕ New Project")
        new_project_btn.clicked.connect(self.create_new_project)
        toolbar.addWidget(new_project_btn)
        self.addToolBar(toolbar)

        # === Database and Tabs ===
        project_name = self.select_project()
        db_manager.switch_project(project_name)
        db_manager.init_db()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # === Inventory-related Tabs ===
        self.asset_tabs = {}
        categories = ["Assets", "Consumables", "Hoses", "Pipe", "Tools", "RCD"]
        for category in categories:
            tab = AssetTab(self.refresh_inventory, self.open_edit_tab, category_filter=category)
            self.asset_tabs[category] = tab  # <- Save the tab for refreshing
            self.tabs.addTab(tab, category)

        # Add Product / Edit Tabs
        self.add_product_tab = AddProductTab(self.refresh_inventory, self.add_category_tab_callback)
        self.tabs.addTab(self.add_product_tab, "Add Item")

        self.edit_items_tab = EditItemsTab(self.refresh_inventory)
        self.tabs.addTab(self.edit_items_tab, "Edit Items")

        # General Inventory Tab
        self.inventory_tab = InventoryTab(self.refresh_inventory, self.open_edit_tab)
        self.tabs.addTab(self.inventory_tab, "Inventory")

    def load_existing_projects(self):
        self.projects = [f.replace(".db", "") for f in os.listdir("projects") if f.endswith(".db")]
        self.project_selector.clear()
        self.project_selector.addItems(self.projects)

    def select_project(self):
        if not self.projects:
            name, ok = QInputDialog.getText(self, "Create New Project", "Enter project name:")
            return name if ok else "Default"
        else:
            name, ok = QInputDialog.getItem(self, "Select Project", "Choose a project:", self.projects, 0, False)
            return name if ok else self.projects[0]

    def switch_project(self, project_name):
        current_project = db_manager.get_current_project_name()
        if current_project != project_name:
            db_manager.switch_project(project_name)
            init_db()
            self.refresh_inventory()

    def open_edit_tab(self, product_id):
        self.tabs.setCurrentWidget(self.edit_items_tab)
        for row in range(self.edit_items_tab.table.rowCount()):
            id_item = self.edit_items_tab.table.item(row, 0)
            if id_item and id_item.text().isdigit() and int(id_item.text()) == product_id:
                self.edit_items_tab.table.selectRow(row)
                self.edit_items_tab.table.scrollToItem(id_item)
                break

    def create_new_project(self):
        name, ok = QInputDialog.getText(self, "New Project", "Project name:")
        if ok and name:
            if not os.path.exists(f"projects/{name}.db"):
                db_manager.switch_project(name)
                init_db()
                self.load_existing_projects()
                self.project_selector.setCurrentText(name)
            else:
                QMessageBox.warning(self, "Error", f"Project '{name}' already exists.")

    def refresh_inventory(self):
        self.edit_items_tab.load_data()
        self.inventory_tab.load_data()
        for category, tab in self.asset_tabs.items():
            tab.load_data()

    def add_category_tab_callback(self, category):
        existing_tabs = [self.tabs.tabText(i) for i in range(self.tabs.count())]
        if category not in existing_tabs:
            new_tab = AssetTab(self.refresh_inventory, self.open_edit_tab, category_filter=category)
            self.asset_tabs[category] = new_tab  # Add to tracking
            self.tabs.addTab(new_tab, category)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.refresh_inventory()
    window.show()
    sys.exit(app.exec())