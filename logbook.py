class Logbook:
    def __init__(self, logbook_path="logbook.txt"):
        self.logbook = logbook_path

    def log_message(self, msg_id):
        with open(self.logbook, "a", encoding="utf-8") as f:
            f.write(f"{msg_id}\n")

    def get_logbook(self):
        with open(self.logbook, "r", encoding="utf-8") as f:
            return f.read().splitlines()

    def trim_logbook(self, percentage):
        logbook = self.get_logbook()
        trimmed_logbook = logbook[int(len(logbook) * percentage) :]
        with open(self.logbook, "w", encoding="utf-8") as f:
            f.write("\n".join(trimmed_logbook))
        return trimmed_logbook
