from pathlib import Path
from datetime import datetime
from todo_item import TodoItem


class Todo:
    def __init__(self, file: Path, index: int | None = None) -> None:
        self.file = file
        self.file_name = f"*new{index}" if self.file.is_dir() else self.file.name
    
    def start(self):
        self.todo_list = self.read_file()
        self.menu()

    def read_file(self) -> list[TodoItem]:
        if self.file.is_dir():
            return []
        else:
            lines = self.file.read_text(encoding="utf8")
            todo_list = []
            for line in lines.split("\n")[:-1]:
                is_done = True if line[0] == "✓" else False
                text = line[28:]
                if is_done:
                    date_start = line.index("[")
                    date_end = line.index("]")
                    done_date_str = line[date_start+1:date_end]
                    done_date = datetime.strptime(done_date_str, "%d/%m/%Y, %H:%M:%S")
                else:
                    done_date = None
                todo_list.append(TodoItem(text, is_done, done_date))
            return todo_list

    def menu(self):
        flag = True
        while flag:
            user_input = input(f"List [{self.file_name}] ~ ")
            match user_input.strip().split(" ", 1):
                case ["add", text]:
                    todoitem = TodoItem(text)
                    self.todo_list.append(todoitem)
                    print("item added.")
                case ["done", rest]:
                    index, status = rest.split(" ")
                    is_success = self.todo_list[int(index)].change_status(status)
                    if is_success:
                        print("item status changed added.")
                    else:
                        print("status could not be changed.")
                case ["list"]:
                    print()
                    for idx, item in enumerate(self.todo_list):
                        print(str(idx) + ".", item)
                    print()
                case ["save"]:
                    if self.file_name.startswith("*"):
                        self.file_name = input("enter file name: ")
                    if self.file.is_dir():
                        self.file = self.file / Path(self.file_name)
                    
                    with open(self.file, "w", encoding="utf8") as f:
                        for todo_item in self.todo_list:
                            f.write(str(todo_item) + "\n")
                case ["save", file_name]:
                    if self.file_name.startswith("*"):
                        self.file_name = file_name
                        self.file = self.file / Path(self.file_name)
                    else:
                        self.file = self.file.parent / Path(file_name)
                    
                    with open(self.file, "w", encoding="utf8") as f:
                        for todo_item in self.todo_list:
                            f.write(str(todo_item) + "\n")
                case ["back"]:
                    flag = False
                case ["help"]:
                    self.print_help()
                case _:
                    print("unsupported input!!")
    
    @staticmethod
    def print_help():
        print(f"\nAvailable commands:")
        print(f" - {'help': <31} print available commands")
        print(f" - {'add [text]': <31} adds new item")
        print(f" - {'done [index] [true|false]': <31} changes status of an item in list")
        print(f" - {'list': <31} list all item")
        print(f" - {'save': <31} save todo list to file with the given name")
        print(f" - {'back': <31} Return to main menu")

    def __str__(self):
        return f"{self.file_name}"
