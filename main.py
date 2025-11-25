import random
import math

# Konstanta
INV_SQRT2 = 0.70710678
INV_PI = 0.31830989

def erf(x):
    # Referensi: https://en.wikipedia.org/wiki/Error_function#Approximation_with_elementary_functions
    p = 0.3275911
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429

    # Karena fungsi erf(x) adalah fungsi ganjil, erf(x) = -erf(-x)
    sign = 1.0
    if (x < 0):
        sign = -1.0
        x = x * -1.0
    t = 1.0 / (1.0 + (p * x))
    result = 1.0 - t*(a1 + t*(a2 + t*(a3 + t*(a4 + t*a5)))) * math.exp(-x*x)

    return sign * result

def phi(x):
    result = 0.5 * (1.0 + erf(x * INV_SQRT2))
    return result

def owens_t(h, a, n):
    # Karena ada integralnya, pakai estimasi dengan jumlah Riemann
    dt = a / n
    area = 0.0
    for i in range(n):
        t = (i + 0.5) * dt
        oprt = (1 + t*t)
        area += (math.exp(-0.5 * h*h * oprt)) / (1 + oprt)
    return area * dt * 0.5 * INV_PI

def skew_norm_cdf(x, xi, omega, alpha):
    z = (x - xi) / omega
    result = phi(z) - 2 * owens_t(z, alpha, 1000)
    return result

def compute_xi(mean, omega=0.2, alpha=5):
    delta = alpha / math.sqrt(1 + alpha*alpha)
    shift = omega * delta * math.sqrt(2 * INV_PI)
    return mean - shift

def main():
    ipk = float(input("Masukkan indeks prestasi kumulatif (IPK) Anda: "))
    print(f"{ipk}")

    # Daftar Peringkat IPK
    # indeks = [random.uniform(2, 4) for _ in range(281)] # untuk sementara membuka daftar indeks pakai algoritma ini
    mean = 3.5
    standard_deviation = 0.20
    probabilitas = skew_norm_cdf(ipk, compute_xi(mean), standard_deviation, alpha = 4)
    print(probabilitas)

if __name__ == "__main__":
    main()
