

class History():
    def __init__(self) -> None:
        self.history = ["1", "2", "3"]
        self.history_max = 10

    def insert(self, content) -> None:
        self.history.insert(0, content)
        if len(self.history) > self.history_max:
            self.history = self.history[0:self.history_max]

    def get(self) -> list:
        return self.history

    def pop(self, index) -> None:
        if len(self.history) > index:
            self.history.pop(index)
