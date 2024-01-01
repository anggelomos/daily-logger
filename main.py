import os
from datetime import datetime, timedelta
from typing import List
from zoneinfo import ZoneInfo

from tickthon import TicktickClient, Task


def format_logs(logs: List[Task], logs_date: str) -> str:
    """Formats the logs of tasks from Ticktick.

    Args:
        logs: A list of Task objects representing the logs.
        logs_date: A string that indicates the date of the logs to be formatted.

    Returns:
        A string representing the formatted logs. Each task is represented by a line that includes the
        task's creation time (in 12-hour format) and title. For example "08:40 AM This is just a day log"
    """
    filtered_logs = [
        log for log in logs if log.created_date.startswith(logs_date)
    ]
    sorted_logs = sorted(filtered_logs, key=lambda x: x.created_date)
    return "\n".join([
        f"- {datetime.fromisoformat(log.created_date).strftime('%-I:%M %p').lower()} {log.title}"
        for log in sorted_logs
    ])


def main():
    delta_days = -1
    ticktick_client = TicktickClient(os.getenv("TT_USER"),
                                     os.getenv("TT_PASS"))

    quebec_timezone = ZoneInfo("America/Toronto")
    logs_date = (datetime.now(quebec_timezone) +
                 timedelta(days=delta_days)).strftime("%Y-%m-%d")

    print("\n### 📟 Day logs")
    print(format_logs(ticktick_client.get_day_logs(), logs_date))
    print("\n### ✨ Day highlights")
    print(format_logs(ticktick_client.get_day_highlights(), logs_date))


if __name__ == "__main__":
    main()
