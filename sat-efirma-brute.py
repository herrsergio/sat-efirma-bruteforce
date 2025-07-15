import subprocess
import itertools

# Ruta al archivo .key de la efirma
key_file = 'llave.key'

# Palabras base, que recuerdes que tiene el passphrase
base_words = ['palabra', 'password', 'ejemplo']

# Prefijos / sufijos / separadores
extras = ['#', '']
separators = [' ', '']

# Leetspeak básico
leet_map = {
    'a': '4',
    'e': '3',
    'i': '1',
    'o': '0',
    's': '5',
    't': '7',
    'c': 'c',
    'd': 'd',
    'h': 'h',
    'H': 'H',
    'S': 'S'
}

def to_leet(word):
    return ''.join(leet_map.get(c, leet_map.get(c.lower(), c)) for c in word)


def casing_variants(word):
    return list(set([
        word.lower(),
        word.upper(),
        word.capitalize()
    ]))

def generate_passwords():
    words = []

    # Para cada palabra base, agrega variantes (minúsculas, mayúsculas, leet)
    for word in base_words:
        variants = casing_variants(word)
        leet_variants = [to_leet(w) for w in variants]
        words.extend(variants + leet_variants)

    passwords = set()

    for w1, w2 in itertools.product(words, words):
        for sep in separators:
            combined = f"{w1}{sep}{w2}"

            for ext in extras:
                passwords.update([
                    combined,
                    f"{ext}{combined}",
                    f"{combined}{ext}",
                    f"{w2}{sep}{w1}",
                    f"{ext}{w2}{sep}{w1}",
                    f"{w2}{sep}{w1}{ext}",
                ])

    # Agrega también palabras solas con extras
    for w in words:
        for ext in extras:
            passwords.add(w)
            passwords.add(f"{ext}{w}")
            passwords.add(f"{w}{ext}")

    return list(passwords)

def test_password(pwd):
    try:
        result = subprocess.run(
            ['openssl', 'rsa', '-in', key_file, '-check', '-noout', '-passin', f'pass:{pwd}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0
    except Exception as e:
        print(f' Error con {pwd}: {e}')
        return False

# Ejecutar
passwords = generate_passwords()
print(f'≡ƒöì Probando {len(passwords)} contraseñas posibles...\n')

for i, pwd in enumerate(passwords, 1):
    print(f'[{i}/{len(passwords)}] 🔑 Probando: {pwd}...')
    if test_password(pwd):
        print(f'\n✅ Contraseña correcta encontrada!: {pwd}')

        # Guardar en archivo por si necesitas luego
        with open('password_encontrada.txt', 'w') as f:
            f.write(pwd + '\n')
        break
else:
    print('\n❌ Ninguna contraseña fue válida.')

