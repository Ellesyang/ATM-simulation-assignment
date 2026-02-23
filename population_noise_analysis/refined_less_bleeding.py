import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cv2

# --- Setup ---
RADIUS = 150  #change this
VMIN_DENSITY = 5  #lower bound, ignores areas with < (number) people/km2 to keep the map "sharp"
#Adjust smoothing: less smoothing for larger maps
SIGMA = 0.1 if RADIUS > 50 else 1.5 

def load_data():
    x_flat = pd.read_csv(r'population_noise_analysis\x_1km.csv', header=None).values.flatten()
    y_flat = pd.read_csv(r'population_noise_analysis\y_1km.csv', header=None).values.flatten()
    pop_flat = pd.read_csv(r'population_noise_analysis\population_1km.csv', header=None).values.flatten()
    
    pop_grid = pop_flat.reshape(1000, 1000)
    extent = [x_flat.min()/1000, x_flat.max()/1000, y_flat.min()/1000, y_flat.max()/1000]
    
    # Coordinates for contouring
    x_axis = np.linspace(x_flat.min(), x_flat.max(), 1000) / 1000
    y_axis = np.linspace(y_flat.max(), y_flat.min(), 1000) / 1000
    X, Y = np.meshgrid(x_axis, y_axis)
    
    return pop_grid, extent, X, Y, pop_flat.max()

def plot_refined():
    pop_grid, extent, X, Y, max_pop = load_data()
    output_dir = "population_noise_analysis/"
    # Apply refined smoothing
    # (0, 0) tells OpenCV to calculate kernel size automatically from sigma
    smoothed = cv2.GaussianBlur(pop_grid, (0, 0), SIGMA)
    
    # 1. Refined Heatmap
    plt.figure(figsize=(10, 8))
    im = plt.imshow(smoothed, extent=extent, cmap='viridis', 
                    norm=LogNorm(vmin=VMIN_DENSITY, vmax=max_pop), 
                    origin='upper', interpolation='bilinear')
    plt.colorbar(im, label=f'People per $km^2$ (Threshold > {VMIN_DENSITY})')
    plt.title(f'Refined Population Map (Radius: {RADIUS}km, Sigma: {SIGMA})')
    
    # 2. Add Detailed Contours
    # Using more levels (30) provides better detail for large-scale maps
    levels = np.logspace(np.log10(VMIN_DENSITY), np.log10(max_pop), 30)
    plt.contour(X, Y, smoothed + 1e-9, levels=levels, colors='white', alpha=0.1, linewidths=0.5)

    # Focus and Mark Schiphol
    plt.xlim(-RADIUS, RADIUS)
    plt.ylim(-RADIUS, RADIUS)
    plt.plot(0, 0, 'rx', label='Schiphol')
    plt.grid(True, linestyle=':', alpha=0.3)
    plt.title(f'Refined Gaussian Smoothing of Population, R={RADIUS}km, vmin={VMIN_DENSITY}, sigma={SIGMA}')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}refined_population_map_{RADIUS}km.png")
    #plt.show()

if __name__ == "__main__":
    plot_refined()