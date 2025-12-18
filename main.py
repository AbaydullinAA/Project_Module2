"""Консольное приложение для шифрования и дешифрования текста."""

import os
import sys
from typing import Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ciphers import (
    read_alphabet, caesar_cipher, vigenere_cipher,
    atbash_cipher, AlphabetError, CipherError
)


def get_alphabet_file() -> str:
    """
    Запрашивает у пользователя путь к файлу с алфавитом.

    Функция в цикле запрашивает у пользователя путь к файлу,
    проверяет его существование и возвращает корректный путь.

    :returns: Путь к файлу с алфавитом
    :rtype: str
    """
    while True:
        filepath = input("Введите путь к файлу с алфавитом: ").strip()
        if os.path.exists(filepath):
            return filepath
        print(f"Ошибка: файл '{filepath}' не найден. Попробуйте снова.")


def select_cipher() -> int:
    """
    Выводит меню выбора шифра и получает выбор пользователя.

    Функция отображает доступные шифры и запрашивает у пользователя
    числовой выбор. Проверяет корректность ввода.

    :returns: Выбранный номер шифра (1-4)
    :rtype: int
    """
    print("\nВыберите шифр:")
    print("1. Шифр Цезаря")
    print("2. Шифр Виженера")
    print("3. Шифр Атбаш")
    print("4. Выход")

    while True:
        try:
            choice = int(input("Ваш выбор (1-4): "))
            if 1 <= choice <= 4:
                return choice
            print("Ошибка: введите число от 1 до 4")
        except ValueError:
            print("Ошибка: введите число")


def get_operation() -> bool:
    """
    Запрашивает операцию (шифрование/дешифрование).

    Функция запрашивает у пользователя выбор операции
    и возвращает соответствующий булевый флаг.

    :returns: True - шифрование, False - дешифрование
    :rtype: bool
    """
    while True:
        op = input("Выберите операцию (1 - шифровать, 2 - дешифровать): ").strip()
        if op == '1':
            return True
        elif op == '2':
            return False
        print("Ошибка: введите 1 или 2")


def get_key(cipher_type: int, encrypt: bool) -> Optional[str]:
    """
    Запрашивает ключ в зависимости от типа шифра.

    Для разных шифров запрашивает разные типы ключей:
    - Цезарь: целое число
    - Виженер: строку
    - Атбаш: не требуется (возвращает None)

    :param cipher_type: Тип шифра (1-3)
    :type cipher_type: int
    :param encrypt: Флаг шифрования (True - шифрование, False - дешифрование)
    :type encrypt: bool
    :returns: Ключ шифрования или None для Атбаш
    :rtype: Optional[str]
    """
    if cipher_type == 1:
        while True:
            try:
                key = int(input("Введите ключ (целое число): "))
                return key
            except ValueError:
                print("Ошибка: ключ должен быть целым числом")

    elif cipher_type == 2:
        action = "шифрования" if encrypt else "дешифрования"
        while True:
            key = input(f"Введите ключ для {action}: ").strip()
            if key:
                return key
            print("Ошибка: ключ не может быть пустым")

    elif cipher_type == 3:
        return None


def get_text() -> str:
    """
    Запрашивает текст для обработки.

    Функция запрашивает у пользователя текст, проверяет,
    что он не пустой, и возвращает его.

    :returns: Введенный текст
    :rtype: str
    """
    while True:
        text = input("Введите текст: ").strip()
        if text:
            return text
        print("Ошибка: текст не может быть пустым")


def main() -> None:
    """
    Основная функция приложения.

    Функция управляет основным циклом работы программы:
    1. Запрашивает файл с алфавитом
    2. В цикле предлагает выбрать шифр, операцию, ввести ключ и текст
    3. Выполняет шифрование/дешифрование
    4. Выводит результат
    5. Предлагает продолжить или выйти

    Обрабатывает основные исключения и выводит понятные сообщения об ошибках.
    """
    print("=" * 50)
    print("Программа для шифрования и дешифрования текста")
    print("=" * 50)

    try:
        alphabet_file = get_alphabet_file()
        alphabet = read_alphabet(alphabet_file)
        print(f"Алфавит загружен ({len(alphabet)} символов)")

        while True:
            cipher_choice = select_cipher()

            if cipher_choice == 4:
                print("Выход из программы.")
                break

            encrypt = get_operation()

            key = get_key(cipher_choice, encrypt)

            text = get_text()

            try:
                if cipher_choice == 1:
                    result = caesar_cipher(text, key, alphabet, encrypt)
                elif cipher_choice == 2:
                    result = vigenere_cipher(text, key, alphabet, encrypt)
                elif cipher_choice == 3:
                    result = atbash_cipher(text, alphabet, encrypt)

                operation = "Зашифрованный" if encrypt else "Расшифрованный"
                print(f"\n{operation} текст:")
                print("-" * 30)
                print(result)
                print("-" * 30)

            except AlphabetError as e:
                print(f"Ошибка в тексте: {e}")
            except CipherError as e:
                print(f"Ошибка шифрования: {e}")

            cont = input("\nПродолжить? (да/нет): ").strip().lower()
            if cont not in ['да', 'д', 'yes', 'y']:
                print("Выход из программы.")
                break

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except AlphabetError as e:
        print(f"Ошибка в алфавите: {e}")
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()