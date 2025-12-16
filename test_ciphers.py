"""Тесты для модуля шифрования."""

import unittest
import tempfile
import os
from ciphers import (
    read_alphabet, validate_text, caesar_cipher,
    vigenere_cipher, atbash_cipher, AlphabetError, CipherError
)


class TestCiphers(unittest.TestCase):
    """Тесты функций шифрования."""

    def setUp(self):
        """Создание временного файла с алфавитом."""
        self.alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

        # Создаем временный файл с алфавитом
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False)
        self.temp_file.write(self.alphabet)
        self.temp_file.close()

    def tearDown(self):
        """Удаление временного файла."""
        os.unlink(self.temp_file.name)

    def test_read_alphabet_success(self):
        """Тест успешного чтения алфавита."""
        result = read_alphabet(self.temp_file.name)
        self.assertEqual(result, self.alphabet)

    def test_read_alphabet_file_not_found(self):
        """Тест чтения несуществующего файла."""
        with self.assertRaises(FileNotFoundError):
            read_alphabet("nonexistent.txt")

    def test_validate_text_success(self):
        """Тест успешной валидации текста."""
        try:
            validate_text("абв", self.alphabet)
            validate_text("а б в", self.alphabet)
        except AlphabetError:
            self.fail("validate_text вызвал исключение на корректном тексте")

    def test_validate_text_invalid_char(self):
        """Тест валидации текста с недопустимым символом."""
        with self.assertRaises(AlphabetError):
            validate_text("abc", self.alphabet)

    def test_caesar_cipher_encrypt_decrypt(self):
        """Тест шифра Цезаря: шифрование и дешифрование."""
        text = "привет"
        key = 3

        # Шифруем
        encrypted = caesar_cipher(text, key, self.alphabet, encrypt=True)
        # Дешифруем
        decrypted = caesar_cipher(encrypted, key, self.alphabet, encrypt=False)

        self.assertEqual(decrypted, text)

    def test_caesar_cipher_with_spaces(self):
        """Тест шифра Цезаря с пробелами."""
        text = "привет мир"
        key = 5

        encrypted = caesar_cipher(text, key, self.alphabet, encrypt=True)
        decrypted = caesar_cipher(encrypted, key, self.alphabet, encrypt=False)

        self.assertEqual(decrypted, text)

    def test_vigenere_cipher_encrypt_decrypt(self):
        """Тест шифра Виженера: шифрование и дешифрование."""
        text = "программирование"
        key = "ключ"

        encrypted = vigenere_cipher(text, key, self.alphabet, encrypt=True)
        decrypted = vigenere_cipher(encrypted, key, self.alphabet, encrypt=False)

        self.assertEqual(decrypted, text)

    def test_vigenere_cipher_empty_key(self):
        """Тест шифра Виженера с пустым ключом."""
        with self.assertRaises(CipherError):
            vigenere_cipher("текст", "", self.alphabet, encrypt=True)

    def test_atbash_cipher_symmetry(self):
        """Тест симметричности шифра Атбаш."""
        text = "шифрование"

        encrypted = atbash_cipher(text, self.alphabet, encrypt=True)
        decrypted = atbash_cipher(encrypted, self.alphabet, encrypt=False)

        self.assertEqual(decrypted, text)

    def test_caesar_cipher_invalid_text(self):
        """Тест шифра Цезаря с недопустимым текстом."""
        with self.assertRaises(AlphabetError):
            caesar_cipher("hello", 1, self.alphabet, encrypt=True)

    def test_vigenere_cipher_invalid_key(self):
        """Тест шифра Виженера с недопустимым ключом."""
        with self.assertRaises(AlphabetError):
            vigenere_cipher("привет", "key", self.alphabet, encrypt=True)


if __name__ == '__main__':
    unittest.main()