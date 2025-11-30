import math

# Konstanta
INV_PI = 0.31830989
INV_SQRT_2 = 0.70710678

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
    result = 0.5 * (1.0 + erf(x * INV_SQRT_2))
    return result

def owens_t(h, a, n):
    # Integralnya dihitung dengan jumlah Riemann
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

def truncated_skew_norm_cdf(x, xi, omega, alpha, min=0.0, max=4.0):
    cdf_min = skew_norm_cdf(min, xi, omega, alpha)
    cdf_max = skew_norm_cdf(max, xi, omega, alpha)
    cdf_x  = skew_norm_cdf(x,  xi, omega, alpha)
    return (cdf_x - cdf_min) / (cdf_max - cdf_min)

def compute_xi(mean, omega, alpha):
    delta = alpha / math.sqrt(1 + alpha*alpha)
    shift = omega * delta * math.sqrt(2 * INV_PI)
    return mean - shift

def main():
    ipk = float(input("Masukkan indeks prestasi kumulatif (IPK) Anda: "))
    print(f"{ipk}")

    mean = 3.84
    alpha = -0.8
    omega = 0.2
    xi = compute_xi(mean, omega, alpha)

    probabilitas = truncated_skew_norm_cdf(ipk, xi, omega, alpha)
    print(round(probabilitas, 4))

if __name__ == "__main__":
    main()
