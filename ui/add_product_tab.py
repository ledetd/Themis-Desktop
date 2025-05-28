from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton
import database

class AddProductTab(QWidget):
    def __init__(self, refresh_callback, add_category_tab_callback):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.add_category_tab_callback = add_category_tab_callback

        self.layout = QVBoxLayout()

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Category")
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

        for widget in [self.category_input, self.name_input, self.number_input, self.description_input, self.quantity_input, self.add_button]:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)

    def add_product(self):
        category = self.category_input.text()
        name = self.name_input.text()
        number = self.number_input.text()
        description = self.description_input.text()
        try:
            quantity = int(self.quantity_input.text())
        except ValueError:
            # Optional: show a warning if quantity isn't valid
            return

        database.add_product(category, name, number, description, quantity)

        # ✅ Safe check before calling the callback
        if self.add_category_tab_callback:
            self.add_category_tab_callback(category)

        self.refresh_callback()

        # Clear inputs
        self.category_input.clear()
        self.name_input.clear()
        self.number_input.clear()
        self.description_input.clear()
        self.quantity_input.clear()