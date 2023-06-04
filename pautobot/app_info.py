import os

__appname__ = "PautoBot"
__description__ = (
    "Private AutoGPT Robot - Your private task assistant with GPT!"
)
__version__ = "0.0.15"

DATA_ROOT = os.path.abspath(
    os.path.join(os.path.expanduser("~"), "pautobot-data")
)
