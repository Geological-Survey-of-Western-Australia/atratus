from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("geo_digital_tools")
except PackageNotFoundError:
    # package is not installed
    pass