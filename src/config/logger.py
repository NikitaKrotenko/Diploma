from src.config.config import Singleton


class Logger(metaclass=Singleton):
    def __init__(self) -> None:
        self.warnings = {}
        self.warnings_log = []
    
    def add_warning(self, name, detains):
        self.warnings[name] = self.warnings.get(name, 0) + 1
        message = f'{name} {detains}'
        self.warnings_log.append(message)
        print(message)

    @property
    def messages(self):
        return self.warnings_log

    @property
    def total(self):
        return len(self.warnings_log)

    @property
    def logs(self):
        return self.warnings
