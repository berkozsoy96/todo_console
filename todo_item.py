from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class TodoItem:
    text: str
    is_done: bool = field(default=False)
    done_time: datetime | None = None

    def change_status(self, status: str) -> bool:
        status = status.lower()
        if status == "true":
            status = True
        elif status == "false":
            status = False
        else:
            print(f"unknown status: {status}")
            return False
        self.is_done = status
        if self.is_done:
            self.done_time = datetime.now()
        else:
            self.done_time = None
        return True
    
    def __str__(self) -> str:
        if self.is_done:
            time_str = f'✓ [{self.done_time.strftime("%d/%m/%Y, %H:%M:%S")}]'
        else:
            time_str = 'X [-]'
        return f"{time_str: <25} - {self.text}"
