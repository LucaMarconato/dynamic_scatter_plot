# Slow rendering when changing the colors of a scatter plot

The dependencies are managed by Conda, so for running the example you can simply use the following:

```
git clone https://github.com/LucaMarconato/dynamic_scatter_plot.git
cd dynamic_scatter_plot
conda env create -f dynamic_scatter_plot.yml
conda activate dynamic_scatter_plot
python dynamic_scatter_plot.py
```

Output:

![](dynamic_scatter_plot.gif)

### Notes
I believe that the rendering could be made more performant since we are changing only the colors of the points and not their positions.
