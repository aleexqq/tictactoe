class GameModel:
    def __init__(self):
        """Инициализация модели игры."""
        self.board_size = 10
        self.current_player = "X"
        self.board = self.initialize_board()

    def initialize_board(self):
        """Создает пустое игровое поле заданного размера."""
        return [[""] * self.board_size for _ in range(self.board_size)]

    def set_board_size(self, size):
        """Изменяет размер игрового поля и сбрасывает его состояние."""
        self.board_size = size
        self.board = self.initialize_board()

    def reset_board(self):
        """Сбрасывает игровое поле в исходное состояние."""
        self.board = self.initialize_board()

    def make_move(self, x, y):
        """Обрабатывает ход игрока по указанным координатам."""
        if 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[y][x] == "":
            self.board[y][x] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def check_winner(self):
        """Проверяет наличие победителя."""
        def check_direction(x, y, dx, dy):
            """Проверяет линию в заданном направлении на наличие победы."""
            symbol = self.board[y][x]
            for i in range(5):
                nx, ny = x + i * dx, y + i * dy
                if not (0 <= nx < self.board_size and 0 <= ny < self.board_size) or self.board[ny][nx] != symbol:
                    return False
            return True

        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] and any(
                    check_direction(x, y, dx, dy) for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]
                ):
                    return True
        return False