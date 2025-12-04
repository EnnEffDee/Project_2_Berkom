import math

INV_PI = 0.31830989
INV_SQRT_2 = 0.70710678
INV_SQRT_PI = 0.56418958

def compute_xi(mean, omega, alpha):
    delta = alpha / math.sqrt(1 + alpha * alpha)
    
    shift = omega * delta * math.sqrt(2 * INV_PI)
    
    return mean - shift

def erf(x):
    return math.erf(x)

def psi(x):
    return INV_SQRT_2 * INV_SQRT_PI * math.exp(-0.5 * x * x)

def phi(x):
    return 0.5 * (1.0 + erf(x * INV_SQRT_2))

def owens_t(h, a, n=1000):
    dt = a / n
    area = 0.0
    for i in range(n):
        t = (i + 0.5) * dt
        oprt = (1 + t*t)
        # Integral dari 1/(1+t^2) * exp(-0.5 * h^2 * (1+t^2))
        area += (math.exp(-0.5 * h*h * oprt)) / (oprt)
    # T(h, a) = (1/2pi) * Integral
    return area * dt * 0.5 * INV_PI

def skew_norm_pdf(x, xi, omega, alpha):
    z = (x - xi) / omega
    return 2 * psi(z) * phi(alpha * z)

def skew_norm_cdf(x, xi, omega, alpha):
    z = (x - xi) / omega
    return phi(z) - 2 * owens_t(z, alpha)

def truncated_skew_norm_pdf(x, xi, omega, alpha, min_val=0.0, max_val=4.0):
    cdf_min = skew_norm_cdf(min_val, xi, omega, alpha)
    cdf_max = skew_norm_cdf(max_val, xi, omega, alpha)
    
    pdf_x = skew_norm_pdf(x, xi, omega, alpha)
    
    return pdf_x / (cdf_max - cdf_min)

def truncated_skew_norm_cdf(x, xi, omega, alpha, min_val=0.0, max_val=4.0):
    cdf_min = skew_norm_cdf(min_val, xi, omega, alpha)
    cdf_max = skew_norm_cdf(max_val, xi, omega, alpha)
    
    cdf_x  = skew_norm_cdf(x, xi, omega, alpha)
    
    return (cdf_x - cdf_min) / (cdf_max - cdf_min)

def inv_truncated_skew_norm_pdf(p, xi, omega, alpha, min_val=0.0, max_val=4.0, tol=1e-6):
    cdf_min = skew_norm_cdf(min_val, xi, omega, alpha)
    cdf_max = skew_norm_cdf(max_val, xi, omega, alpha)

    target = cdf_min + p * (cdf_max - cdf_min)

    i, f = min_val, max_val
    
    if p <= 0:
        return min_val
    if p >= 1:
        return max_val
    
    while f - i > tol:
        mid = 0.5 * (i + f)
        cdf_mid = skew_norm_cdf(mid, xi, omega, alpha)
        
        if cdf_mid < target:
            i = mid
        else:
            f = mid
            
    return 0.5 * (i + f)
