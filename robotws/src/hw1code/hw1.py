import math
import matplotlib.pyplot as plt
import numpy as np

a = 2
b = 6
c = 5
d = 7

def theta(phi):
    gamma = np.arctan2(c * np.sin(phi), d + c * np.cos(phi))
    cos_beta = (a**2 - b**2 + c**2 + d**2 + 2 * c * d * np.cos(phi)) / (2*a* np.sqrt(c**2 + d**2 + 2 * c * d * np.cos(phi)))
    if -1 <= cos_beta <= 1:
        gamma = np.arctan2(c * np.sin(phi), d + c * np.cos(phi))
        beta = np.arccos(cos_beta)
        return [gamma + beta, gamma-beta]
    else:
        return None

phi_range = np.linspace(-2 * np.pi, 2 * np.pi, 100000)
theta_range_pos = [theta(phi)[0] if theta(phi) is not None else None for phi in phi_range] 
theta_range_neg = [theta(phi)[1] if theta(phi) is not None else None for phi in phi_range]
theta_range_pos_shift1 = [theta + 2*np.pi if theta is not None else None for theta in theta_range_pos]
theta_range_neg_shift1 = [theta + 2*np.pi if theta is not None else None for theta in theta_range_neg]
theta_range_pos_shift2 = [theta - 2*np.pi if theta is not None else None for theta in theta_range_pos]

theta_range_neg_shift2 = [theta - 2*np.pi if theta is not None else None for theta in theta_range_neg]


plt.plot(phi_range, theta_range_pos)
plt.plot(phi_range, theta_range_neg)
plt.plot(phi_range, theta_range_pos_shift1)
plt.plot(phi_range, theta_range_neg_shift1)
plt.plot(phi_range, theta_range_pos_shift2)
plt.plot(phi_range, theta_range_neg_shift2)
plt.xlabel(r'$\phi$')
plt.ylabel(r'$\theta$')
plt.title(f'Configuration Space of 4-bar Linkage for a = {a}')

plt.xlim(-2 * np.pi, 2 * np.pi)
plt.ylim(-2 * np.pi, 2 * np.pi)

x_ticks =[-2*np.pi, -3/2*np.pi, -1*np.pi, -1/2*np.pi, 0, 1/2*np.pi, 1*np.pi, 3/2*np.pi, 2*np.pi]
x_labels = ['-2π', '-3π/2', '-π', '-π/2', 0, 'π/2', 'π', '3π/2', '2π']

y_ticks =[-2*np.pi, -3/2*np.pi, -1*np.pi, -1/2*np.pi, 0, 1/2*np.pi, 1*np.pi, 3/2*np.pi, 2*np.pi]
y_labels = ['-2π', '-3π/2', '-π', '-π/2', 0, 'π/2', 'π', '3π/2', '2π']

plt.xticks(x_ticks,x_labels)
plt.yticks(y_ticks,y_labels)

plt.grid(True)
plt.show()
