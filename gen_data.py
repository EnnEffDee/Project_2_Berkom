import math_functions
import csv

# File ini tidak termasuk bagian dari hasil tubes karena di luar 
def main():
    n = int(input("Masukkan jumlah data yang ingin digenerate: "))
    mean = float(input("Masukkan mean data yang ingin digenerate: "))
    nama_file = input("Masukkan nama filenya: ")
    array = [0.0 for i in range(n)]

    alpha = -0.8
    omega = 0.2

    xi = math_functions.compute_xi(mean, omega, alpha)

    for i in range(n):
        p = (i + 0.5) / n
        array[i] = round(math_functions.inv_truncated_skew_norm_pdf(p, xi, omega, alpha), 2)
        print(array[i], end=" ")
    
    with open(nama_file, "w", newline="") as f:
        writer = csv.writer(f)
        for x in array:
            writer.writerow([x])

if __name__ == "__main__":
    main()
