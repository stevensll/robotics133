import math
import matplotlib.pyplot as plt
import numpy as np

a = 6
b = 6
c = 5
d = 7

def theta(phi):
    gamma = np.arctan2(c * np.sin(phi), d + c * np.cos(phi))
    cos_beta = a**2 - b**2 + c**2 + d**2 + 2 * c * d * np.cos(phi)
    if -1 <= cos_beta <= 1:
        gamma = np.arctan2(c * np.sin(phi), d + c * np.cos(phi))
        beta = np.arccos(a**2 - b**2 + c**2 + d**2 + 2 * c * d * np.cos(phi))
        return gamma + beta
    else:
        return None

phi_range = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
theta_range = [theta(phi) for phi in phi_range]

plt.plot(phi_range, theta_range)
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
