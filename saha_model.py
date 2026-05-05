import numpy as np
import matplotlib.pyplot as plt

# C
R_sun = 6.96e8
M_sun = 1.989e30
day_to_sec = 86400
m_p = 1.67e-27
pi = np.pi
k_B = 1.38e-23
h = 6.626e-34
m_e = 9.11e-31
eV_to_J = 1.602e-19

# Parameters
v_exp = 200e3
R_WD = 0.012 * R_sun
M_ej = 8.0e-5 * M_sun
f_Li = 1.5e-5
T0 = 11000
tau_cool = 8.0
n_e0 = 1e12

# Time grid
t_days = np.linspace(0.1, 40, 500)
t_sec = t_days * day_to_sec
R_shell = v_exp * t_sec

# Temperature (using exponential cooling, one could test different cooling laws)
T_e = T0 * np.exp(-t_days / tau_cool)
T_e = np.maximum(T_e, 3000)

# Electron density
n_e = n_e0 * (t_days / 1.0)**(-3)
n_e = np.maximum(n_e, 1e8)

# Saha equation
chi_LiI = 5.39 * eV_to_J
U_LiI = 2.0
U_LiII = 1.0

kT = k_B * T_e
saha_prefactor = (2 * U_LiII / U_LiI) * (2 * np.pi * m_e * kT / h**2)**(1.5)
saha_factor = (saha_prefactor / n_e) * np.exp(-chi_LiI / kT)
f_LiI = 1 / (1 + saha_factor)

# Maximum value
max_f_LiI = np.max(f_LiI)
f_LiI_at_10 = f_LiI[np.argmin(np.abs(t_days - 10))]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(t_days, f_LiI, 'r-', lw=2.5, label=r'$f_{\mathrm{LiI}}$ (Saha equation)')
ax.set_xlim(0, 40)
ax.set_ylim(1e-12, 1e-3)
ax.tick_params(axis='y', labelsize=18)
ax.tick_params(axis='x', labelsize=18)
ax.set_yscale('log')
ax.set_xlabel("Time (D)", fontsize=18)
ax.set_ylabel(r"Neutral Lithium Fraction $f_{\mathrm{LiI}}$", fontsize=18)
ax.set_title("Neutral Lithium Fraction from Saha Equation", fontsize=18)
ax.legend(loc='upper right', fontsize=12)
plt.show()
