import datetime
import settings

LOG_LEVEL = 4  # 4 is most verbose, 0 is least verbose (no output), 1 is normal operations
# ANSI color codes
RESET = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'


def _current_time():
    return datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")


def info(message, level):
    if level <= LOG_LEVEL:
        enriched_message = f"[*][{_current_time()}] {message}"
        write_log_to_file(enriched_message)
        print(f"{enriched_message}")


def success(message, level):
    if level <= LOG_LEVEL:
        enriched_message = f"[+][{_current_time()}] {message}"
        write_log_to_file(enriched_message)
        print(f"{GREEN}{enriched_message}{RESET}")


def error(message, level):
    if level <= LOG_LEVEL:
        enriched_message = f"[-][{_current_time()}] {message}"
        write_log_to_file(enriched_message)
        print(f"{RED}{enriched_message}{RESET}")


def debug(message, level):
    if level <= LOG_LEVEL:
        enriched_message = f"[D][{_current_time()}] {message}"
        write_log_to_file(enriched_message)
        print(f"{YELLOW}{enriched_message}{RESET}")


def write_log_to_file(message):
    with open(settings.LOG_PATH, "a") as file:
        file.write("\n"+message)