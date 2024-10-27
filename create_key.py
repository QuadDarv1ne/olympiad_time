import hashlib

def create_hash(data: str, algorithm: str = 'sha256') -> str:
    """Создает хеш для заданных данных с использованием выбранного алгоритма.

    Args:
        data (str): Данные для хеширования.
        algorithm (str): Алгоритм хеширования ('sha256' или 'sha512').

    Returns:
        str: Хешированные данные в шестнадцатеричном формате.
    """
    # Выбор алгоритма
    if algorithm == 'sha256':
        hash_object = hashlib.sha256()
    elif algorithm == 'sha512':
        hash_object = hashlib.sha512()
    else:
        raise ValueError("Unsupported algorithm. Use 'sha256' or 'sha512'.")

    # Обновление объекта хеша данными
    hash_object.update(data.encode('utf-8'))
    
    # Возврат хеша в шестнадцатеричном формате
    return hash_object.hexdigest()

# Пример использования
data = "Пример текста для хеширования"
sha256_hash = create_hash(data, 'sha256')
sha512_hash = create_hash(data, 'sha512')

print(f"SHA-256: {sha256_hash}")
print(f"SHA-512: {sha512_hash}")
