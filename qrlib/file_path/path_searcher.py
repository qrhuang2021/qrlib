import os


class PathSearcher:
    def __init__(self, root='.'):
        assert os.path.isdir(root)
        self._root = root

    def all_path(self, special_extensions=None):
        if isinstance(special_extensions, str):
            special_extensions = [special_extensions]
        result = []
        for root, _, filenames in sorted(os.walk(self._root, followlinks=True)):
            for filename in filenames:
                if self._is_special_file(filename, special_extensions):
                    result.append(os.path.join(root, filename))
        return result

    def all_image_path(self):
        SPECIAL_EXTENSIONS = [
            '.jpg', '.JPG', '.jpeg', '.JPEG',
            '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
            '.tif', '.TIF', '.tiff', '.TIFF', '.webp',
        ]
        return self.all_path(SPECIAL_EXTENSIONS)

    def _is_special_file(self, filename, special_extensions):
        if special_extensions is None:
            return True
        else:
            return any(filename.endswith(extension) for extension in special_extensions)
