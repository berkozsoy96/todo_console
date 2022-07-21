from todo import Todo
from pathlib import Path


class App:
    def __init__(self, folder_path: str = "todos") -> None:
        self.folder_path = Path(folder_path)
        self.file_list = self.read_files()
    
    def start(self):
        self.menu()

    def menu(self) -> None:
        flag = True
        while flag:
            user_input = input(f"App [{self.folder_path}] ~ ")
            match user_input.strip().split(" ", 1):
                case ["new"]:
                    count = 1
                    for file in self.file_list:
                        if file.file_name.startswith("*"):
                            count += 1
                    new_todo = Todo(self.folder_path, index=count)
                    new_todo.start()
                    self.file_list.append(new_todo)
                case ["open", file_name_or_index]:
                    if file_name_or_index.isdigit():
                        self.file_list[int(file_name_or_index)].start()
                    else:
                        index = [file.file_name for file in self.file_list].index(file_name_or_index)
                        self.file_list[index].start()
                case ["list"]:
                    print()
                    for idx, file in enumerate(self.file_list):
                        print(str(idx) + ".", file)
                    print()
                case ["exit"]:
                    flag = False
                case ["help"]:
                    self.print_help()
                case [command]:
                    print(f"Unrecognized command: '{command}'. Type 'help' if you want to see available commands.")

    @staticmethod
    def print_help():
        print(f"\nAvailable commands:")
        print(f" - {'help': <31} print available commands")
        print(f" - {'new ': <31} create new to-do list")
        print(f" - {'list': <31} list all files")
        print(f" - {'open [file_name | index]': <31} existing to-do list")
        print(f" - {'exit ': <31} exit :D")

    def read_files(self) -> list[Todo]:
        return [Todo(file) for file in self.folder_path.iterdir()]


if __name__ == "__main__":
    a = App("todo_app/todos")
    a.start()
