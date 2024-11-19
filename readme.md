Hi
# Shell Emulator

## Описание

**Shell Emulator** — это простое графическое приложение, эмулирующее выполнение базовых команд оболочки внутри виртуальной файловой системы, извлечённой из архива `.tar`. Программа позволяет:
- Выполнять команды `ls`, `cd`, `mkdir`, `uniq`.
- Работать в контексте директории, смонтированной из указанного архива `.tar`.
- Автоматически выполнять команды из стартового скрипта.

Приложение имеет графический интерфейс на основе библиотеки `tkinter`.

---

## Функционал

### Основные возможности
1. **Выполнение команд оболочки:**
   - `ls` — просмотр содержимого текущей директории.
   - `cd <path>` — переход в указанную директорию.
   - `mkdir <dirname>` — создание новой директории.
   - `uniq <filename>` — вывод уникальных строк файла.

2. **Работа с архивами:**
   - Извлечение указанного `.tar`-архива в виртуальную файловую систему.
   - Выполнение всех команд в контексте виртуальной директории.

3. **Стартовый скрипт:**
   - Автоматическое выполнение списка команд из файла при запуске программы.

4. **Графический интерфейс:**
   - Поле ввода для команд.
   - Поле вывода для результатов выполнения.

---

## Настройки

Настройки указываются в файле `config.ini`. Пример файла:

```ini
[Settings]
username = user                # Имя пользователя, отображаемое в приложении
computername = my_computer     # Имя компьютера, отображаемое в приложении
archive_path = path/to/archive.tar # Путь к .tar-архиву, который нужно извлечь
start_script = path/to/start_script.txt # Путь к стартовому скрипту