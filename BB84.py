import random

def generate_message(n):
    return [random.randint(0, 1) for _ in range(n)]

def generate_bases(n):
    return [random.randint(0, 1) for _ in range(n)]

def measure_qubits(alice_message, alice_bases, bob_bases):
    measured_bits = []
    for i in range(len(alice_message)):
        if alice_bases[i] == bob_bases[i]:
            measured_bits.append(alice_message[i])
        else:
            measured_bits.append(random.randint(0, 1))
    return measured_bits

def get_polarization_arrow(basis, bit):
    if basis == 0:  # Базис ➕
        return "↕" if bit == 0 else "↔"
    else:  # Базис ❌
        return "↗" if bit == 0 else "↖"

def bb84_protocol(n=25):
    alice_message = generate_message(n)
    print(f"Сообщение Алисы:\n   {alice_message}")
    
    alice_bases = generate_bases(n)
    alice_bases_str = ['➕' if b == 0 else '❌' for b in alice_bases]
    print(f"Базисы Алисы:\n   {alice_bases_str}")
    
    alice_polarization = [get_polarization_arrow(alice_bases[i], alice_message[i]) for i in range(n)]
    print(f"Поляризация:\n   {alice_polarization}")
    
    bob_bases = generate_bases(n)
    bob_bases_str = ['➕' if b == 0 else '❌' for b in bob_bases]
    print(f"Базисы Боба:\n   {bob_bases_str}")
    
    bob_measured = measure_qubits(alice_message, alice_bases, bob_bases)
    print(f"Измеренные Бобом биты:\n   {bob_measured}")
    
    sift_key = [str(bob_measured[i]) if alice_bases[i] == bob_bases[i] else '-' for i in range(n)]
    
    print(f"Итог:\n   {sift_key}")

if __name__ == "__main__":
    bb84_protocol(25)
