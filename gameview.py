from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from game_model import GameModel
from statisticsview import StatisticsDialog
import time


class GameView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("5 в ряд")

        # Модель игры
        self.model = GameModel()

        # Сетка для кнопок
        self.grid_layout = QGridLayout(self)
        self.setLayout(self.grid_layout)

        # Виджеты для отображения таймеров
        self.timer_label_x = QLabel("60", self)
        self.timer_label_o = QLabel("60", self)
        self.timer_label_x.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.timer_label_o.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.timer_label_x.setAlignment(Qt.AlignCenter)
        self.timer_label_o.setAlignment(Qt.AlignCenter)

        self.timer_text_x = QLabel("Игрок X", self)
        self.timer_text_o = QLabel("Игрок O", self)
        self.timer_text_x.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.timer_text_o.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.timer_layout = QVBoxLayout()
        self.timer_layout.addWidget(self.timer_text_x)
        self.timer_layout.addWidget(self.timer_label_x)
        self.timer_layout.addWidget(self.timer_text_o)
        self.timer_layout.addWidget(self.timer_label_o)

        self.buttons = []
        self.init_board()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def init_board(self):
        """Инициализирует игровое поле."""

        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.buttons = []
        size = self.model.board_size
        self.grid_layout.addLayout(self.timer_layout, 0, size, 2, 1)
        self.reset_timers()
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
            self.model.update_time()

    def update_button(self, x, y):
        """Обновляет текст кнопки в зависимости от состояния клетки."""
        self.buttons[y][x].setText(self.model.board[y][x])

    def reset_game(self):
        """Сбрасывает игру и обновляет вид."""
        self.model.reset_board()
        self.init_board()

    def reset_timers(self):
        """Сбрасывает таймеры на начальное значение (60 секунд) для обоих игроков."""
        self.model.reset_timers()
        self.timer_label_x.setText("60")
        self.timer_label_o.setText("60")

    def set_board_size(self, size):
        """Устанавливает размер игрового поля."""
        self.model.set_board_size(size)
        self.init_board()

    def update_timer(self):
        """Обновляет отображение таймера."""
        self.model.update_time()

        time_left_x = int(self.model.time_left["X"])
        time_left_o = int(self.model.time_left["O"])

        self.timer_label_x.setText(str(time_left_x))
        self.timer_label_o.setText(str(time_left_o))

        if self.model.time_up():
            winner = "O" if self.model.current_player == "X" else "X"
            QMessageBox.information(self, "Время вышло!", f"{winner} победил! (Время истекло)")
            StatisticsDialog.add_to_statistics(winner)
            self.reset_game()
