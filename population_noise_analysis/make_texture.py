import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cv2

def create_texture():
    # Load data
    
    pop_data = pd.read_csv('population_1km.csv', header=None).values
    pop_grid = pop_data.reshape(1000, 1000)

    # Smooth the data for a better "contour" look
    # (Using 2.0 for a balance between detail and clarity)
    smoothed = cv2.GaussianBlur(pop_grid, (0, 0), 2.0)

    # Create figure with NO borders or axes
    fig = plt.figure(figsize=(10, 10), frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    # Define color levels (logarithmic)
    # vmin=10 hides empty areas/oceans to keep the map clean
    vmin, vmax = 10, pop_grid.max()
    levels = np.logspace(np.log10(vmin), np.log10(vmax), 20)

    # Generate the filled contours with transparency
    ax.contourf(smoothed, levels=levels, cmap='viridis', 
                norm=LogNorm(vmin=vmin, vmax=vmax), alpha=0.7)

    # Save as transparent PNG
    plt.savefig('pop_density_texture.png', transparent=True, dpi=300, 
                bbox_inches='tight', pad_inches=0)
    print("Texture saved as pop_density_texture.png")

if __name__ == "__main__":
    create_texture()