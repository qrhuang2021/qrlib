import matplotlib.pyplot as plt


class ImageComposer:
    def __init__(self, nrows, ncols, max_dpi=1000):
        self._nrows = nrows
        self._ncols = ncols
        self._max_dpi = max_dpi
        self._min_dpi = 100

    def save(self, output_path, image_path_list, title_list):
        assert len(image_path_list) == len(title_list)
        fig, axs = plt.subplots(nrows=self._nrows, ncols=self._ncols,
                                # figsize=(w, h),
                                constrained_layout=False,
                                subplot_kw={'xticks': [], 'yticks': []})
        for ax, image_path, title in zip(axs.flat, image_path_list, title_list):
            grid = plt.imread(image_path)
            # ax.imshow(grid, interpolation=interp_method, cmap='viridis')
            ax.imshow(grid)
            ax.set_title(str(title))

        for dpi in range(self._max_dpi, self._min_dpi-1, -100):
            try:
                plt.savefig(output_path, dpi=dpi)
            except:
                continue
            else:
                break