import logging
import sys

def setup_logger(level=logging.INFO):
    """Mengkonfigurasi logger untuk output ke console.

    Fungsi ini mengatur logger dengan format yang mudah dibaca dan mengirimkan output
    ke konsol. Logger akan dikonfigurasi dengan level logging yang dapat disesuaikan.

    Args:
        level (int, optional): Level logging yang digunakan. 
                              Defaultnya adalah logging.INFO.

    Returns:
        None: Fungsi ini tidak mengembalikan nilai, hanya mengatur konfigurasi logger.

    Contoh:
        >>> setup_logger(logging.DEBUG)
        >>> logging.debug("Pesan debug")
        >>> logging.info("Pesan informasi")
    """
    log_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.setLevel(level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)

    root_logger.addHandler(console_handler)