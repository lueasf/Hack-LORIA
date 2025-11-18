import time


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def compute_primes(limit):
    primes = []
    for n in range(2, limit + 1):
        if is_prime(n):
            primes.append(n)
    return primes


def main():
    start = time.time()
    print("Démarrage du calcul des nombres premiers...")
    limit = 200000
    primes = compute_primes(limit)
    end = time.time()
    print(f"Nombre de premiers <= {limit} : {len(primes)}")
    print(f"Temps de calcul : {end - start:.3f} secondes")


if __name__ == "__main__":
    main()