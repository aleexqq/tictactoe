from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        """Диалог настроек размера поля."""
        super().__init__(parent)
        self.setWindowTitle("Настройки")

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Размер поля (10 или 20):", self))

        self.size_selector = QComboBox(self)
        self.size_selector.addItems(["10", "20"])
        layout.addWidget(self.size_selector)

        save_button = QPushButton("Сохранить", self)
        save_button.clicked.connect(self.accept)
        layout.addWidget(save_button)

    def get_board_size(self):
        """Возвращает выбранный размер поля."""
        return int(self.size_selector.currentText())
