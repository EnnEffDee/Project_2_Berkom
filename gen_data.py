import math
import csv

# Konstanta
INV_PI = 0.31830989
INV_SQRT_2 = 0.70710678
INV_SQRT_PI = 0.56418958

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

def compute_xi(mean, omega, alpha):
    delta = alpha / math.sqrt(1 + alpha*alpha)
    shift = omega * delta * math.sqrt(2 * INV_PI)
    return mean - shift

def psi(x):
    return INV_SQRT_2 * INV_SQRT_PI * math.exp(-0.5 * x * x)

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

def skew_norm_pdf(x, xi, omega, alpha):
    z = (x - xi) / omega
    result_psi = psi(z)
    result_phi = phi(alpha * z)
    result = (2 / omega) * result_psi * result_phi
    return result

def skew_norm_cdf(x, xi, omega, alpha):
    z = (x - xi) / omega
    result = phi(z) - 2 * owens_t(z, alpha, 1000)
    return result

def truncated_skew_norm_pdf(x, xi, omega, alpha, min=0.0, max=4.0):
    cdf_min = skew_norm_cdf(min, xi, omega, alpha)
    cdf_max = skew_norm_cdf(max, xi, omega, alpha)
    pdf_x = skew_norm_pdf(x, xi, omega, alpha)
    return pdf_x / (cdf_max - cdf_min)


def truncated_skew_norm_pdf_inv(p, xi, omega, alpha, min=0.0, max=4.0, tol=1e-6):
    cdf_min = skew_norm_cdf(min, xi, omega, alpha)
    cdf_max = skew_norm_cdf(max, xi, omega, alpha)

    target = cdf_min + p * (cdf_max - cdf_min)

    i, f = min, max
    while f - i > tol:
        mid = 0.5 * (i + f)
        cdf_mid = skew_norm_cdf(mid, xi, omega, alpha)
        if cdf_mid < target:
            i = mid
        else:
            f = mid
    return 0.5 * (i + f)

def main():
    n = int(input("Masukkan jumlah data yang ingin digenerate: "))
    mean = float(input("Masukkan mean data yang ingin digenerate: "))
    nama_file = input("Masukkan nama filenya: ")
    array = [0.0 for i in range(n)]

    mean = 3.84
    alpha = -0.8
    omega = 0.2

    xi = compute_xi(mean, omega, alpha)

    for i in range(n):
        p = (i + 0.5) / n
        array[i] = round(truncated_skew_norm_pdf_inv(p, xi, omega, alpha), 2)
    
    with open(nama_file, "w", newline="") as f:
        writer = csv.writer(f)
        for x in array:
            writer.writerow([x])

if __name__ == "__main__":
    main()
