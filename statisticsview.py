import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


class StatisticsDialog(QDialog):
    def __init__(self, parent=None):
        """Диалоговое окно для отображения статистики побед."""
        super().__init__(parent)
        self.setWindowTitle("Статистика")
        self.stats_file = "statistics.json"

        # Основной макет
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Метка для отображения статистики
        self.stats_label = QLabel()
        self.stats_label.setText("Статистика отсутствует.")
        layout.addWidget(self.stats_label)

        # Кнопка очистки статистики
        clear_button = QPushButton("Очистить статистику", self)
        clear_button.clicked.connect(self.clear_statistics)
        layout.addWidget(clear_button)

        # Загрузка данных
        self.load_statistics()

    def load_statistics(self):
        """Загружает данные из файла и обновляет метку."""
        try:
            with open(self.stats_file, "r") as file:
                stats = json.load(file)
            self.stats_label.setText(self.format_statistics(stats))
        except FileNotFoundError:
            self.stats_label.setText("Статистика отсутствует.")

    def clear_statistics(self):
        """Очищает файл статистики."""
        with open(self.stats_file, "w") as file:
            json.dump({}, file)
        self.stats_label.setText("Статистика отсутствует.")

    def format_statistics(self, stats):
        """Форматирует данные статистики для отображения."""
        if not stats:
            return "Статистика отсутствует."
        result = "Статистика побед:\n"
        for player, wins in stats.items():
            result += f"{player}: {wins} побед\n"
        return result

    @staticmethod
    def add_to_statistics(winner):
        """Обновляет статистику, добавляя победителя."""
        stats_file = "statistics.json"
        try:
            with open(stats_file, "r") as file:
                stats = json.load(file)
        except FileNotFoundError:
            stats = {}

        stats[winner] = stats.get(winner, 0) + 1

        with open(stats_file, "w") as file:
            json.dump(stats, file)
