from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from game_model import GameModel
from statisticsview import StatisticsDialog


class GameView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("5 в ряд")

        # Модель игры
        self.model = GameModel()

        # Сетка для кнопок
        self.grid_layout = QGridLayout(self)
        self.setLayout(self.grid_layout)

        # Создаем игровое поле
        self.buttons = []
        self.init_board()

    def init_board(self):
        """Инициализирует кнопки игрового поля."""
        # Удаляем старые кнопки
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.buttons = []
        size = self.model.board_size
        for y in range(size):
            row = []
            for x in range(size):
                button = QPushButton("")
                button.setFixedSize(40, 40)
                button.setStyleSheet(
                    "font-size: 16px; font-weight: bold; border: 1px solid black;"
                )
                button.clicked.connect(self.create_click_handler(x, y))
                self.grid_layout.addWidget(button, y, x)
                row.append(button)
            self.buttons.append(row)

    def create_click_handler(self, x, y):
        """Создает обработчик для кнопки с заданными координатами."""
        def handler():
            self.make_move(x, y)
        return handler

    def make_move(self, x, y):
        """Обрабатывает ход игрока и обновляет вид кнопки."""
        if self.model.make_move(x, y):
            self.update_button(x, y)
            if self.model.check_winner():
                winner = "O" if self.model.current_player == "X" else "X"
                QMessageBox.information(self, "Победа!", f"Победил {winner}!")
                StatisticsDialog.add_to_statistics(winner)
                self.reset_game()

    def update_button(self, x, y):
        """Обновляет текст кнопки в зависимости от состояния клетки."""
        self.buttons[y][x].setText(self.model.board[y][x])

    def reset_game(self):
        """Сбрасывает игру и обновляет вид."""
        self.model.reset_board()
        self.init_board()

    def set_board_size(self, size):
        """Устанавливает размер игрового поля."""
        self.model.set_board_size(size)
        self.init_board()
