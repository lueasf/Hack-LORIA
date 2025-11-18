class Main {
	public static void main(String[] args) {
		int repetitions = 1;
		if (args.length > 0) {
			try {
				repetitions = Integer.parseInt(args[0]);
			} catch (Exception e) {
				System.err.println("Argument non numérique, utilisation de 1 répétition.");
			}
		}

		System.out.println("Début du test Java - répétitions = " + repetitions);
		long t0 = System.currentTimeMillis();

		long totalPrimes = 0;
		for (int r = 0; r < repetitions; r++) {
			totalPrimes += countPrimes(2000000); // ajuster pour modifier la charge
		}

		long t1 = System.currentTimeMillis();
		System.out.println("Total primes (somme) : " + totalPrimes);
		System.out.println("Durée (ms) : " + (t1 - t0));
		System.out.println("Fin du test Java");
	}

	// compte le nombre de nombres premiers <= n (algorithme simple pour la charge CPU)
	static int countPrimes(int n) {
		int count = 0;
		for (int i = 2; i <= n; i++) {
			if (isPrime(i)) count++;
		}
		return count;
	}

	static boolean isPrime(int x) {
		if (x < 2) return false;
		if (x % 2 == 0) return (x == 2);
		int r = (int) Math.sqrt(x);
		for (int d = 3; d <= r; d += 2) {
			if (x % d == 0) return false;
		}
		return true;
	}
}
