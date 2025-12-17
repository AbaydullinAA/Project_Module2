"""Модуль для шифрования и дешифрования текста."""

import os
from typing import Optional


class CipherError(Exception):
    """
    Базовое исключение для ошибок шифрования.

    :ivar message: Сообщение об ошибке
    :type message: str
    """
    pass


class AlphabetError(CipherError):
    """
    Ошибка при работе с алфавитом.

    Наследуется от CipherError.

    :ivar message: Сообщение об ошибке
    :type message: str
    """
    pass


def read_alphabet(filepath: str) -> str:
    """
    Читает алфавит из файла.

    Функция открывает файл по указанному пути, считывает его содержимое,
    проверяет корректность алфавита и возвращает его в виде строки.

    :param filepath: Путь к файлу с алфавитом
    :type filepath: str
    :returns: Строка, содержащая символы алфавита
    :rtype: str
    :raises FileNotFoundError: Если файл не найден по указанному пути
    :raises AlphabetError: Если алфавит пуст или содержит дубликаты символов
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            alphabet = f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл с алфавитом не найден: {filepath}")

    if not alphabet:
        raise AlphabetError("Алфавит не может быть пустым")

    if len(alphabet) != len(set(alphabet)):
        raise AlphabetError("Алфавит содержит повторяющиеся символы")

    return alphabet

def validate_text(text: str, alphabet: str) -> None:
    """
    Проверяет, что все символы текста есть в алфавите.

    Функция проходит по каждому символу текста и проверяет его наличие
    в переданном алфавите. Пробелы игнорируются.

    :param text: Текст для проверки
    :type text: str
    :param alphabet: Алфавит для проверки
    :type alphabet: str
    :raises AlphabetError: Если найден символ не из алфавита
    """
    for char in text:
        if char not in alphabet and char != ' ':
            raise AlphabetError(f"Символ '{char}' не найден в алфавите")


def caesar_cipher(text: str, key: int, alphabet: str, encrypt: bool = True) -> str:
    """
    Шифрует или дешифрует текст с помощью шифра Цезаря.

    Шифр Цезаря — это простой шифр подстановки, в котором каждый символ
    в тексте заменяется символом, находящимся на некотором постоянном числе
    позиций левее или правее него в алфавите.

    :param text: Текст для обработки
    :type text: str
    :param key: Ключ шифрования (сдвиг)
    :type key: int
    :param alphabet: Алфавит для шифрования
    :type alphabet: str
    :param encrypt: Флаг операции (True - шифрование, False - дешифрование)
    :type encrypt: bool
    :returns: Обработанный текст
    :rtype: str
    :raises AlphabetError: Если текст содержит символы не из алфавита
    """
    validate_text(text, alphabet)

    n = len(alphabet)
    result = []

    for char in text:
        if char == ' ':
            result.append(' ')
            continue

        idx = alphabet.index(char)
        if encrypt:
            new_idx = (idx + key) % n
        else:
            new_idx = (idx - key) % n

        result.append(alphabet[new_idx])

    return ''.join(result)


def vigenere_cipher(text: str, key: str, alphabet: str, encrypt: bool = True) -> str:
    """
    Шифрует или дешифрует текст с помощью шифра Виженера.

    Шифр Виженера — это метод полиалфавитного шифрования, в котором
    для шифрования используется ключевое слово. Каждая буква ключа
    определяет сдвиг в алфавите для соответствующей буквы текста.

    :param text: Текст для обработки
    :type text: str
    :param key: Ключ шифрования
    :type key: str
    :param alphabet: Алфавит для шифрования
    :type alphabet: str
    :param encrypt: Флаг операции (True - шифрование, False - дешифрование)
    :type encrypt: bool
    :returns: Обработанный текст
    :rtype: str
    :raises AlphabetError: Если текст или ключ содержат символы не из алфавита
    :raises CipherError: Если ключ пустой
    """
    validate_text(text, alphabet)
    validate_text(key, alphabet)

    if not key:
        raise CipherError("Ключ не может быть пустым")

    n = len(alphabet)
    result = []
    key = key.replace(' ', '')

    for i, char in enumerate(text):
        if char == ' ':
            result.append(' ')
            continue

        text_idx = alphabet.index(char)
        key_idx = alphabet.index(key[i % len(key)])

        if encrypt:
            new_idx = (text_idx + key_idx) % n
        else:
            new_idx = (text_idx - key_idx) % n

        result.append(alphabet[new_idx])

    return ''.join(result)


def atbash_cipher(text: str, alphabet: str, encrypt: bool = True) -> str:
    """
    Шифрует или дешифрует текст с помощью шифра Атбаш.

    Шифр Атбаш — это простой шифр подстановки, в котором алфавит
    переворачивается. Первая буква алфавита заменяется на последнюю,
    вторая — на предпоследнюю и так далее.

    Примечание: Для шифра Атбаш шифрование и дешифрование одинаковы.

    :param text: Текст для обработки
    :type text: str
    :param alphabet: Алфавит для шифрования
    :type alphabet: str
    :param encrypt: Не используется, оставлен для совместимости интерфейса
    :type encrypt: bool
    :returns: Обработанный текст
    :rtype: str
    :raises AlphabetError: Если текст содержит символы не из алфавита
    """
    validate_text(text, alphabet)

    reversed_alphabet = alphabet[::-1]
    result = []

    for char in text:
        if char == ' ':
            result.append(' ')
            continue

        idx = alphabet.index(char)
        result.append(reversed_alphabet[idx])

    return ''.join(result)