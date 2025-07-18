from datetime import datetime

class Logger:
    name = ""
    def set_logger_name(self, name):
        self.name = name

    def __send(self, level, msg):
        if not self.name:
            self.name = self.__class__.__name__
        
        print(f"[{datetime.now().strftime("%H:%M:%S")}] [{self.name}/{level}]: {msg}")

    def debug(self, msg): self.__send("DBUG", msg)
    def info(self, msg): self.__send("INFO", msg)
    def warn(self, msg): self.__send("WARN", msg)
    def error(self, msg): self.__send("EROR", msg)
    def critical(self, msg): self.__send("CRIT", msg)
