import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


# Load the data
x = pd.read_csv(r'population_noise_analysis\x_1km.csv', header=None).values.flatten()
y = pd.read_csv(r'population_noise_analysis\y_1km.csv', header=None).values.flatten()
pop = pd.read_csv(r'population_noise_analysis\population_1km.csv', header=None).values.flatten()

# Reshape population into a 1000x1000 grid
pop_grid = pop.reshape(1000, 1000)

# Define extent in km
extent = [x.min()/1000, x.max()/1000, y.min()/1000, y.max()/1000]

# Plotting
plt.figure(figsize=(10, 10))
im = plt.imshow(pop_grid, extent=extent, cmap='viridis', 
                norm=LogNorm(vmin=1, vmax=pop.max()), origin='upper')

plt.colorbar(im, label='Population per $km^2$')
plt.title('Population Density in a 15km Radius Around Schiphol (1 km x 1 km grid)')
plt.xlabel('X distance from Schiphol (km)')
plt.ylabel('Y distance from Schiphol (km)')

# Mark Schiphol (Origin)
plt.plot(0, 0, 'rx', markersize=10, label='Schiphol (Origin)')
plt.legend()

# Focus on the relevant Netherlands region
plt.xlim(-150, 150) #change this!
plt.ylim(-150, 150) #change this!
plt.grid(True, linestyle=':', alpha=0.5)
plt.savefig('population_density_map.png')
plt.show()

