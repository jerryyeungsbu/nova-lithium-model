import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# C
R_sun = 6.96e8
M_sun = 1.989e30
day_to_sec = 86400
m_p = 1.67e-27
pi = np.pi
sigma = 5.67e-8

# Adjust based on your data
v_exp = 300e3        # m/s (expansion velocity)
R_WD = 0.012 * R_sun # m (white dwarf radius)
M_ej = 1.0e-7 * M_sun # kg (ejected mass)
f_Li = 1.0e-5        # lithium mass fraction
T_ph = 10000         # K (photospheric temperature)
d = 1.2e3 * 3.086e16 # m (distance)
t_max = 40           # days (max time to plot)

# Generic flux data (Adjust based on your data)
t_flux = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40])
flux = np.array([1e-11, 2e-11, 4e-11, 7e-11, 1e-10, 1.5e-10, 2e-10, 2.5e-10,
                 3e-10, 3.5e-10, 4e-10, 5e-10, 4.5e-10, 3.5e-10, 2.5e-10, 1.5e-10, 1e-10])

# Time grid
t_days = np.linspace(0.1, t_max, 500)
t_sec = t_days * day_to_sec
R_shell = v_exp * t_sec

# f_cov
f_cov = np.where(R_shell > R_WD, R_WD / R_shell, 1.0)

# Interpolate flux to get R_ph
cs = CubicSpline(t_flux, flux, extrapolate=True)
flux_interp = cs(t_days)
flux_interp = np.maximum(flux_interp, 1e-20)

# Photospheric radius
L = 4 * pi * d**2 * flux_interp
R_ph = np.sqrt(L / (4 * pi * sigma * T_ph**4))

# f_vis
offset = 0.1 * R_sun
f_vis = np.zeros_like(t_days)
for i in range(len(t_days)):
    R = R_shell[i]
    Rph = R_ph[i]
    if R > 0:
        f_vis[i] = (R - Rph + offset) / R
        f_vis[i] = max(0, min(f_vis[i], 1))
        f_vis[i] = f_vis[i]**0.5

# Total lithium atoms
M_Li = M_ej * f_Li
N_Li_total = M_Li / (7 * 1.67e-27)

# 7Be deca
lambda_decay = np.log(2) / 53.22
f_Be_decayed = 1 - np.exp(-lambda_decay * t_days)
N_Li_at_t = N_Li_total * f_Be_decayed

# Geometric dilution
N_geom = N_Li_at_t / (4 * pi * R_shell**2) / 1e4

# Final model
N_model = N_geom * f_vis * f_cov

# Plot
plt.figure(figsize=(10, 6))
plt.plot(t_days, N_model, 'b-', lw=3, label='Model Prediction')
plt.xlabel("Time (days)", fontsize=18)
plt.ylabel(r"N(Li I) [cm$^{-2}$]", fontsize=18)
plt.yscale('log')
plt.xlim(0, 10)
plt.ylim(1e6, 1e18)
plt.title(f"Model Prediction", fontsize=18)
plt.legend(fontsize=12)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()
