# Created on 20210127 by HighTemplar-wjiang
# Some colors for good looking plots. 

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


class preset_params:
    
    # Colors for points, lines.
    mpl_color_list_curves = [
        "#cf625b", # Red-like,
        "#51a8cf", # Blue-like,
        "#50bf57", # Green-like
    ]

    # Colors for fill-in. 
    mpl_color_list_fillins = [
        "#64c9f5", # Light blue
        "#f57e76", # Light red
    ]

    # Pre-settings for figures.

    # 2 figures per row.
    ax_label_params_small = {
        "fontsize": 14,
        "fontstyle": "italic",
        "fontweight": "bold"
    }
    tick_label_params_small = {
        "fontsize": 12,
        "fontweight": "bold"
    }

    # 3 figures per row.
    ax_label_params_normal = {
        "fontsize": 20,
        "fontstyle": "italic",
        "fontweight": "bold"
    }
    tick_label_params_normal = {
        "fontsize": 18,
        "fontweight": "bold"
    }

    # 4 figures per row.
    ax_label_params_large = {
        "fontsize": 30,
        "fontstyle": "italic",
        "fontweight": "bold"
    }
    
    tick_label_params_large = {
        "fontsize": 28,
        "fontweight": "bold"
    }

# Master class for colors.
class MPLColors:
        
    def __init__(self, cmap, norm=None, nbins=256, ncolors=0, name="mycolormap", gamma=1.0,
                 shuffle_segments=False, shuffle_listed=False):
        
        self._nbins = nbins
        self._colors = None
        self._ncolors = ncolors
        
        # Create normalizer if not provided.
        if norm is None:
            self._norm = mpl.colors.Normalize(vmin=0.0, vmax=1.0)
        else:
            self._norm = norm
        
        # Get / create color map according to the parameter types.
        if type(cmap) is str:
            # Load color map.
            mpl_cmap = mpl.cm.get_cmap(cmap)
            
            # Check type and get color list.
            cmap_class = type(mpl_cmap)
            if cmap_class is mpl.colors.ListedColormap:
                self._colors = mpl_cmap.colors
            elif cmap_class is mpl.colors.LinearSegmentedColormap:
                ncolors = 10 if ncolors == 0 else ncolors
                self._colors = [mpl_cmap(value) for value in np.linspace(0, 1.0, ncolors)]
            else:
                raise NotImplementedError("Unknown color map class {}.".format(str(cmap_class)))
            
        elif type(cmap) is tuple:
            self._colors = list(cmap)
        else:
            # Wrong type.
            raise TypeError("Init function only accepts cmap or tuple.")
            
        # Set number of colors.
        self._ncolors = len(self._colors) if self._ncolors == 0 else self._ncolors
        
        # Shuffle listed map is flag.
        self._colors = list(self._colors)
        self._shuffled_colors = np.random.permutation(self._colors)
            
        # Re-generate color maps from color list.
        if shuffle_segments:
            self._segmented_cmap = mpl.colors.LinearSegmentedColormap.from_list(
                name, self._shuffled_colors, N=nbins, gamma=gamma)
        else:
            self._segmented_cmap = mpl.colors.LinearSegmentedColormap.from_list(
                name, self._colors, N=nbins, gamma=gamma)
            
        # Get colors with gamma correction.
        self._corrected_colors = [self._segmented_cmap(value) for value in np.linspace(0, 1.0, self._ncolors)]
        self._shuffled_corrected_colors = np.random.permutation(self._corrected_colors)
            
        if shuffle_listed:
            self._listed_cmap = mpl.colors.ListedColormap(self._shuffled_corrected_colors, N=None)
        else:
            self._listed_cmap = mpl.colors.ListedColormap(self._corrected_colors, N=None)
    
    def show_colormap(self):
        """Plot both continuous and quantified color maps."""
        # Prepare data.
        x_bins = np.linspace(0.0, 1.0, self._nbins).reshape(1, -1)
        x_sets = np.linspace(0.0, 1.0, self._ncolors).reshape(1, -1)
        
        # Prepare axes.
        fig, axes = plt.subplots(nrows=2, figsize=(10, 1))
        for ax in axes:
            ax.set_axis_off()
        
        # Show segmented color map.
        axes[0].imshow(x_bins, cmap=self._segmented_cmap, norm=self._norm, aspect="auto")
        
        # Show quantified color map.
        axes[1].imshow(x_sets, cmap=self._listed_cmap, norm=self._norm, aspect="auto")
        
        fig.tight_layout()
        
    def get_color(self, value):
        """Return a color w.r.t. the value."""
        if type(value) is float:
            # Return from the continuous color map for a float value.
            return self._segmented_cmap(self._norm(value))
        
        elif type(value) is int:            
            # Return from the quantified color map for an int value.
            return self._listed_cmap(value)
        
    def get_color_list(self):
        """Return a list of quantified colors."""
        return self._listed_cmap.colors
    
    def __add__(self, other):
        """Override add operation."""
        return MPLColors(tuple(self.get_color_list() + other.get_color_list()))
    
    def __getitem__(self, key):
        """Return a quantified color indexed by key if integer,
           otherwise, return a color from normalized colormap."""
        return self.get_color(key)
            
    def __iter__(self):
        """Return quantifed color list for iterations."""
        return self._listed_cmap_colors
        

