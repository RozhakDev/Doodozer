import argparse
import asyncio
import logging
from urllib.parse import urlparse

from doodoo.core.downloader import Doodozer
from doodoo.utils.helper import setup_logger

def is_valid_url(url: str) -> bool:
    """Memvalidasi apakah string merupakan URL yang valid.

    Metode ini memeriksa apakah string yang diberikan mengandung komponen URL yang 
    valid, seperti scheme dan netloc.

    Args:
        url (str): String URL yang akan divalidasi.

    Returns:
        bool: True jika URL valid, False jika tidak valid.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

async def main():
    """Fungsi utama untuk menjalankan Doodozer CLI.

    Fungsi ini mengatur argumen command line, memvalidasi URL (satu atau beberapa dengan pemisah koma),
    menginisialisasi logger, dan memulai proses pengunduhan video dari DoodStream.

    Returns:
        None: Fungsi ini tidak mengembalikan nilai.

    Raises:
        SystemExit: Jika tidak ada URL yang valid atau terjadi kesalahan fatal.

    Contoh:
        Dijalankan dari command line:
        $ python main.py https://d-s.io/e/xxxxxxxxxx
        $ python main.py https://d-s.io/e/xxxxxxxxxx -o video.mp4 -v
        $ python main.py "https://d-s.io/e/xxxxxxxxxx,https://d-s.io/e/yyyyyyyyyy" -o videos/
    """
    parser = argparse.ArgumentParser(
        description="Doodozer CLI - Alat Pengunduh Video dari DoodStream.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Contoh penggunaan:\n"
               "  python main.py https://d-s.io/e/xxxxxxxxxx\n"
               "  python main.py https://d-s.io/e/xxxxxxxxxx -o my_video.mp4 -v\n"
               "  python main.py \"https://d-s.io/e/xxxxxxxxxx,https://d-s.io/e/yyyyyyyyyy\" -o videos/"
    )

    parser.add_argument("url", metavar="URL", type=str, help="URL video DoodStream yang akan diunduh. Bisa menggunakan beberapa URL dengan pemisah koma (contoh: url1,url2).")
    parser.add_argument("-o", "--output", dest="output_path", type=str, default=None, help="Nama file atau path untuk menyimpan video. Jika tidak disertakan, nama file akan dibuat otomatis.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Aktifkan mode verbose untuk output log yang lebih detail.")
    parser.add_argument("--no-progress", action="store_true", help="Nonaktifkan progress bar saat mengunduh.")

    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logger(log_level)

    urls = [url.strip() for url in args.url.split(",")]
    
    valid_urls = []
    for url in urls:
        if not is_valid_url(url) or ("/e/" not in url and "/d/" not in url):
            logging.warning(f"URL tidak valid dan akan diabaikan: {url}")
        else:
            valid_urls.append(url)
    
    if not valid_urls:
        logging.error("Tidak ada URL DoodStream yang valid. Pastikan URL berasal dari DoodStream.")
        return
    
    logging.info(f"Mengunduh {len(valid_urls)} video...")

    try:
        if len(valid_urls) > 1 and args.output_path and not args.output_path.endswith("/") and not args.output_path.endswith("\\"):
            import os
            output_dir = args.output_path
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)
                logging.info(f"Membuat direktori: {output_dir}")
                args.output_path = output_dir
            else:
                args.output_path = output_dir

        for i, url in enumerate(valid_urls, 1):
            logging.info(f"Memproses video {i}/{len(valid_urls)}: {url}")
            
            if len(valid_urls) > 1:
                if args.output_path and os.path.isdir(args.output_path):
                    current_output_path = args.output_path
                elif args.output_path:
                    current_output_path = os.path.dirname(args.output_path) or "."
                else:
                    current_output_path = "."
            else:
                current_output_path = args.output_path
            
            downloader = Doodozer(
                url=url,
                output_path=current_output_path,
                show_progress=not args.no_progress
            )
            await downloader.download()
            
            logging.info(f"Selesai mengunduh video {i}/{len(valid_urls)}")
            
        logging.info("Semua video berhasil diunduh!")
    except Exception as e:
        logging.error(f"Terjadi kesalahan yang tidak terduga: {e}")
    except asyncio.CancelledError:
        logging.info("Program dihentikan oleh asyncio")

if __name__ == "__main__":
    asyncio.run(main())