LOGBOOK = "logbook.txt"


def log_message(msg_id):
    with open(LOGBOOK, "a", encoding="utf-8") as f:
        f.write(f"{msg_id}\n")


def get_logbook():
    with open(LOGBOOK, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def trim_logbook(percentage, logbook):
    trimmed_logbook = logbook[int(len(logbook) * percentage):]
    with open(LOGBOOK, "w", encoding="utf-8") as f:
        f.write("\n".join(trimmed_logbook))
    return trimmed_logbook
