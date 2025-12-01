import math
import csv

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
        area += (math.exp(-0.5 * h*h * oprt)) / (oprt)
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
    nama_jurusan = ["Informatika Ganesha", "Informatika Jatinangor", "Sistem dan Teknologi Informasi Ganesha", "Sistem dan Teknologi Informasi Jatinangor"]
    mean_if_g = 3.84
    mean_if_j = 3.68
    mean_sti_g = 3.71
    mean_sti_j = 3.61
    data_ipk_total = [0.0 for i in range(285)]
    data_ipk_if_g = [0.0 for i in range(72)]
    data_ipk_if_j = [0.0 for i in range(71)]
    data_ipk_sti_g = [0.0 for i in range(71)]
    data_ipk_sti_j = [0.0 for i in range(71)]
    alpha = -0.8
    omega = 0.2

    ipk = float(input("Masukkan indeks prestasi kumulatif (IPK) Anda: "))

    pilihan = int(input("Apa yang ingin Anda lakukan?\n1. Menampilkan nilai indeks angkatan\n2. Menghitung peluang memasuki jurusan\n3. Keluar"))
    if pilihan == 1:
        k = 0
        with open("data_ipk_total.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                data_ipk_total[k] = row
                k += 1

        k = 0
        with open("data_ipk_if_g.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                data_ipk_if_g[k] = row
                k += 1

        k = 0
        with open("data_ipk_if_j.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                data_ipk_if_j[k] = row
                k += 1

        k = 0
        with open("data_ipk_sti_g.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                data_ipk_sti_g[k] = row
                k += 1

        k = 0
        with open("data_ipk_sti_j.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                data_ipk_sti_j[k] = row
                k += 1

        print("============\nRanking data\n============")
        print("Peingkat IPK Seangkatan")
        for i in range(285):
            print(f"Peringkat #{i}: {data_ipk_total[i]}")
        print("Peingkat IPK Informatika Ganesha")
        for i in range(72):
            print(f"Peringkat #{i}: {data_ipk_if_g[i]}")
        print("Peingkat IPK Informatika Jatinangor")
        for i in range(71):
            print(f"Peringkat #{i}: {data_ipk_if_j[i]}")
        print("Peingkat IPK Sistem dan Teknologi Informasi Ganesha")
        for i in range(71):
            print(f"Peringkat #{i}: {data_ipk_sti_g[i]}")
        print("Peingkat IPK Sistem dan Teknologi Informasi Jatinangor")
        for i in range(71):
            print(f"Peringkat #{i}: {data_ipk_sti_j[i]}")

    elif pilihan == 2:
        print("\nJurusan:\n1. Informatika Ganesha\n2.Informatika Jatinangor\n3. Sistem dan Teknologi Informasi Ganesha\n4. Sistem dan Teknologi Informasi Jatinangor")
        pilihan = [0 for i in range(4)]
        for i in range(4):
            pilihan[i] = int(input(f"Pilihan {i + 1}: "))

        xi_if_g = compute_xi(mean_if_g, omega, alpha)
        xi_if_j = compute_xi(mean_if_j, omega, alpha)
        xi_sti_g = compute_xi(mean_sti_g, omega, alpha)
        xi_sti_j = compute_xi(mean_sti_j, omega, alpha)

        probabilitas = [0 for i in range(4)]
        for i in range(4):
            if pilihan[i] == 1:
                probabilitas[i] = truncated_skew_norm_cdf(ipk, xi_if_g, omega, alpha)
            if pilihan[i] == 2:
                probabilitas[i] = truncated_skew_norm_cdf(ipk, xi_if_j, omega, alpha)
            if pilihan[i] == 3:
                probabilitas[i] = truncated_skew_norm_cdf(ipk, xi_sti_g, omega, alpha)
            if pilihan[i] == 4:
                probabilitas[i] = truncated_skew_norm_cdf(ipk, xi_sti_j, omega, alpha)
        
        print("Jadi, probabilitasmu untuk memasuki masing-masing jurusan adalah ")
        for i in range(4):
            print(f"{i + 1}. Pilihan {i + 1} \"{nama_jurusan[pilihan[i] - 1]}\": {round(probabilitas[i], 4)}")

if __name__ == "__main__":
    main()
