from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox
import database

class AddProductTab(QWidget):
    def __init__(self, refresh_callback, add_category_tab_callback):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.add_category_tab_callback = add_category_tab_callback

        self.layout = QVBoxLayout()

        # Define categories here or pass dynamically if you want
        self.categories = ["Assets", "Consumables", "Hoses", "Pipe", "Tools", "RCD"]

        self.category_selector = QComboBox()
        self.category_selector.addItems(self.categories)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Item Name")
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Part Number")
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")

        self.add_button = QPushButton("Add Item")
        self.add_button.clicked.connect(self.add_product)

        for widget in [
            self.category_selector,
            self.name_input,
            self.number_input,
            self.description_input,
            self.quantity_input,
            self.add_button
        ]:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)

    def add_product(self):
        category = self.category_selector.currentText()
        name = self.name_input.text()
        number = self.number_input.text()
        description = self.description_input.text()
        try:
            quantity = int(self.quantity_input.text())
        except ValueError:
            # Optional: show a warning if quantity isn't valid
            return

        database.add_product(category, name, number, description, quantity)

        if self.add_category_tab_callback:
            self.add_category_tab_callback(category)

        self.refresh_callback()

        # Clear inputs (for QComboBox, reset to first)
        self.category_selector.setCurrentIndex(0)
        self.name_input.clear()
        self.number_input.clear()
        self.description_input.clear()
        self.quantity_input.clear()