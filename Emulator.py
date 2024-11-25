import os
import tarfile
import tempfile
import tkinter as tk
from tkinter import messagebox
from configparser import ConfigParser


class ShellEmulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Shell Emulator")

        # Поле вывода
        self.output_text = tk.Text(self.master, height=15, width=70, wrap='word')
        self.output_text.pack(padx=10, pady=10)

        # Конфигурация
        self.load_config()

        # Текущая директория
        self.current_dir = os.getcwd()

        # Поле ввода команды
        self.command_entry = tk.Entry(self.master, width=70)
        self.command_entry.pack(padx=10, pady=(0, 10))
        self.command_entry.bind("<Return>", self.execute_command)

        # Виртуальная директория
        self.virtual_dir = None
        self.setup_virtual_directory()
        self.execute_start_script()
        
    def load_config(self):
        config = ConfigParser()
        config_file = 'config.ini'

        if not os.path.exists(config_file):
            messagebox.showerror("Ошибка", f"Файл конфигурации '{config_file}' не найден.")
            self.master.quit()
            return

        config.read(config_file)

        self.username = config.get('Settings', 'username', fallback='user')
        self.computername = config.get('Settings', 'computername', fallback='computer')
        self.archive_path = config.get('Settings', 'archive_path', fallback='')
        self.start_script_path = config.get('Settings', 'start_script', fallback='')

    def setup_virtual_directory(self):
        """Извлекает архив в виртуальную директорию."""
        if not self.archive_path or not os.path.exists(self.archive_path):
            self.output_text.insert(tk.END, f"Архив '{self.archive_path}' не найден. Работа в текущей директории.\n")
            return

        try:
            self.virtual_dir = tempfile.mkdtemp()  # Создаём временную директорию
            with tarfile.open(self.archive_path, 'r') as tar:
                tar.extractall(self.virtual_dir)  # Извлекаем архив во временную папку
            self.current_dir = self.virtual_dir
            self.output_text.insert(tk.END, f"Архив '{self.archive_path}' извлечён в виртуальную директорию.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Ошибка извлечения архива: {e}\n")

    def execute_start_script(self):
        """Выполняет команды из стартового скрипта."""
        if not self.start_script_path:
            self.output_text.insert(tk.END, "Стартовый скрипт не указан в конфигурации.\n")
            return
        
        if not os.path.exists(self.start_script_path):
            self.output_text.insert(tk.END, f"Стартовый скрипт '{self.start_script_path}' не найден.\n")
            return
        
        try:
            with open(self.start_script_path, 'r') as script_file:
                commands = script_file.readlines()
                
            self.output_text.insert(tk.END, f"Выполнение стартового скрипта: {self.start_script_path}\n")
            for command in commands:
                command = command.strip()
                if command:
                    self.output_text.insert(tk.END, f"Стартовая команда: {command}\n")
                    self.command_entry.delete(0, tk.END)
                    self.command_entry.insert(0, command)
                    self.execute_command()  # Выполняем каждую команду
        except Exception as e:
            self.output_text.insert(tk.END, f"Ошибка выполнения стартового скрипта: {e}\n")


    def execute_command(self, event=None):
        command = self.command_entry.get().strip()
        self.command_entry.delete(0, tk.END)

        if not command:
            return  # Игнорировать пустые команды

        self.output_text.insert(tk.END, f"> {command}\n")

        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == "ls":
            self.ls(args)
        elif cmd == "cd":
            self.cd(args)
        elif cmd == "exit":
            self.exit_shell()
        elif cmd == "mkdir":
            self.mkdir(args)
        elif cmd == "uniq":
            self.uniq(args)
        else:
            self.output_text.insert(tk.END, f"Неизвестная команда: {cmd}\n")

    def ls(self, args):
        try:
            path = self.current_dir
            if args:
                path = os.path.join(self.current_dir, args[0])
            files = os.listdir(path)
            files_sorted = sorted(files)
            self.output_text.insert(tk.END, "\n".join(files_sorted) + "\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Ошибка: {e}\n")

    def cd(self, args):
        if not args:
            self.output_text.insert(tk.END, "Использование: cd <путь>\n")
            return
        try:
            new_path = args[0]
            if not os.path.isabs(new_path):
                new_path = os.path.join(self.current_dir, new_path)
            if not os.path.isdir(new_path):
                raise FileNotFoundError(f"Директория '{new_path}' не найдена.")
            self.current_dir = new_path
            self.output_text.insert(tk.END, f"Текущая директория: {self.current_dir}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Ошибка: {e}\n")

    def mkdir(self, args):
        if not args:
            self.output_text.insert(tk.END, "Использование: mkdir <имя_директории>\n")
            return
        try:
            dir_name = args[0]
            new_dir_path = os.path.join(self.current_dir, dir_name)
            os.mkdir(new_dir_path)
            self.output_text.insert(tk.END, f"Директория '{dir_name}' создана\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Ошибка: {e}\n")

    def uniq(self, args):
        if not args:
            self.output_text.insert(tk.END, "Использование: uniq <имя_файла>\n")
            return
        try:
            filename = args[0]
            file_path = os.path.join(self.current_dir, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                unique_lines = list(dict.fromkeys(line.strip() for line in lines))
            self.output_text.insert(tk.END, "\n".join(unique_lines) + "\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Ошибка: {e}\n")

    def exit_shell(self):
        self.master.quit()
        if self.virtual_dir:
            import shutil
            shutil.rmtree(self.virtual_dir)  # Удаляем временную директорию


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = ShellEmulator(root)
    root.mainloop()
