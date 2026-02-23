import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cv2
import os

# --- setup ---
RADIUS = 150  #change this depending on where we're looking (smaller radius more refined)
PATH_X = r'population_noise_analysis\x_1km.csv'
PATH_Y = r'population_noise_analysis\y_1km.csv'
PATH_POP = r'population_noise_analysis\population_1km.csv'

def load_data():
    #Load the data once inside the function
    x_flat = pd.read_csv(PATH_X, header=None).values.flatten()
    y_flat = pd.read_csv(PATH_Y, header=None).values.flatten()
    pop_flat = pd.read_csv(PATH_POP, header=None).values.flatten()
    
    pop_grid = pop_flat.reshape(1000, 1000)
    
    extent = [x_flat.min()/1000, x_flat.max()/1000, y_flat.min()/1000, y_flat.max()/1000]
    
    #Create 1000-point axes for the meshgrid
    x_axis = np.linspace(x_flat.min(), x_flat.max(), 1000) / 1000
    y_axis = np.linspace(y_flat.max(), y_flat.min(), 1000) / 1000
    X, Y = np.meshgrid(x_axis, y_axis)
    
    return pop_grid, extent, X, Y, pop_flat.max()

def run_all_plots():
    pop_grid, extent, X, Y, max_pop = load_data()
    output_dir = "population_noise_analysis/"
    
    #Sanity check
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #1. Raw Population Density Plot
    plt.figure(figsize=(10, 8))
    im1 = plt.imshow(pop_grid, extent=extent, cmap='viridis', 
                     norm=LogNorm(vmin=1, vmax=max_pop), origin='upper')
    plt.colorbar(im1, label='Population per $km^2$')
    plt.title(f'Raw Population Density ({RADIUS}km Radius)')
    plt.xlim(-RADIUS, RADIUS)
    plt.ylim(-RADIUS, RADIUS)
    plt.plot(0, 0, 'rx', markersize=10, label='Schiphol')
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend()
    plt.savefig(f"{output_dir}plot_raw_{RADIUS}km.png")
    print(f"Saved: {output_dir}plot_raw_{RADIUS}km.png")

    #2. Smoothed Population Density Plot
    smoothed = cv2.GaussianBlur(pop_grid, (7, 7), 1.5)
    plt.figure(figsize=(10, 8))
    im2 = plt.imshow(smoothed, extent=extent, cmap='viridis', 
                     norm=LogNorm(vmin=1, vmax=max_pop), 
                     origin='upper', interpolation='bilinear')
    plt.colorbar(im2, label='Population per $km^2$')
    plt.title(f'Smoothed Population Density ({RADIUS}km Radius)')
    plt.xlim(-RADIUS, RADIUS)
    plt.ylim(-RADIUS, RADIUS)
    plt.plot(0, 0, 'rx', markersize=10, label='Schiphol')
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend()
    plt.savefig(f"{output_dir}plot_smoothed_{RADIUS}km.png")
    print(f"Saved: {output_dir}plot_smoothed_{RADIUS}km.png")

    #3. Contour Density Map
    plt.figure(figsize=(10, 8))
    levels = np.logspace(0, np.log10(max_pop), 20)
    cp = plt.contourf(X, Y, smoothed + 1e-9, levels=levels, cmap='viridis', norm=LogNorm())
    plt.colorbar(cp, label='Population Density Surface')
    plt.title(f'Contour Density Map ({RADIUS}km Radius)')
    plt.xlim(-RADIUS, RADIUS)
    plt.ylim(-RADIUS, RADIUS)
    plt.plot(0, 0, 'rx', markersize=10, label='Schiphol')
    plt.grid(True, linestyle=':', alpha=0.3)
    plt.legend()
    plt.savefig(f"{output_dir}plot_contour_{RADIUS}km.png")
    print(f"Saved: {output_dir}plot_contour_{RADIUS}km.png")

#Execute
if __name__ == "__main__":
    run_all_plots()