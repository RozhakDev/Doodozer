import logging
import os
from typing import Optional

import aiohttp
import aiofiles
from tqdm.asyncio import tqdm

from doodoo.api.doodstream import DoodStreamAPI

class Doodozer:
    """Kelas utama untuk mengorkestrasi proses pengunduhan video dari DoodStream.

    Kelas ini menyediakan antarmuka lengkap untuk mengunduh video dari DoodStream,
    mulai dari mendapatkan URL unduhan hingga menyimpan file dengan progress bar.

    Attributes:
        url (str): URL video DoodStream yang akan diunduh.
        output_path (Optional[str]): Path file output. Jika None, nama file akan dibuat otomatis.
        show_progress (bool): Menampilkan progress bar jika True.
        logger (logging.Logger): Logger untuk logging aktivitas pengunduhan.
    """

    def __init__(self, url: str, output_path: Optional[str] = None, show_progress: bool = True):
        """Menginisialisasi instance Doodozer Downloader.

        Args:
            url (str): URL video DoodStream yang akan diunduh.
            output_path (Optional[str]): Path file output. Jika None, nama file akan dibuat
                otomatis berdasarkan judul video. Jika merupakan direktori, file akan disimpan
                di dalam direktori tersebut dengan nama otomatis.
            show_progress (bool): Menampilkan progress bar jika True. Defaultnya adalah True.

        Raises:
            ValueError: Jika URL yang diberikan tidak valid atau kosong.
        """
        self.url = url
        self.output_path = output_path
        self.show_progress = show_progress
        self.logger = logging.getLogger(__name__)
    
    async def download(self) -> None:
        """Memulai seluruh proses pengunduhan video dari DoodStream.

        Metode ini mengorkestrasi seluruh proses pengunduhan, mulai dari:
        1. Mengambil informasi video (URL unduhan langsung dan judul)
        2. Menentukan path output file
        3. Mengunduh file dengan progress bar (jika diaktifkan)
        4. Menyimpan file ke lokasi yang ditentukan

        Returns:
            None: Metode ini bersifat asinkron dan tidak mengembalikan nilai.

        Raises:
            aiohttp.ClientError: Jika terjadi kesalahan jaringan saat mengakses DoodStream.
            Exception: Kesalahan lainnya yang mungkin terjadi selama proses pengunduhan.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            api = DoodStreamAPI(session)

            result = await api.get_download_url(self.url)
            if not result:
                self.logger.error("Gagal mendapatkan informasi video. Proses dihentikan.")
                return
            
            direct_url, title = result

            if self.output_path:
                if os.path.isdir(self.output_path):
                    filename = f"{title}.mp4"
                    final_path = os.path.join(self.output_path, filename)
                else:
                    final_path = self.output_path
            else:
                filename = f"{title}.mp4"
                final_path = filename
            
            self.logger.info(f"Video akan disimpan di: {os.path.abspath(final_path)}")

            await self._download_file(session, direct_url, final_path)

    async def _download_file(self, session: aiohttp.ClientSession, url: str, path: str) -> None:
        """Mengunduh file dari URL dan menyimpannya ke path yang diberikan dengan progress bar.

        Metode ini mengunduh file asinkron menggunakan HTTP streaming dan menampilkan
        progress bar jika show_progress diaktifkan. File akan diunduh dalam chunk
        untuk mengurangi penggunaan memori.

        Args:
            session (aiohttp.ClientSession): Session HTTP untuk melakukan request.
            url (str): URL file yang akan diunduh.
            path (str): Path lengkap di mana file akan disimpan.

        Returns:
            None: Metode ini bersifat asinkron dan tidak mengembalikan nilai.

        Raises:
            aiohttp.ClientError: Jika terjadi kesalahan jaringan saat mengunduh.
            OSError: Jika terjadi kesalahan saat menulis file ke disk.
            Exception: Kesalahan lainnya yang mungkin terjadi selama proses pengunduhan.

        Note:
            Jika terjadi kesalahan selama pengunduhan, file yang sudah diunduh
            akan dihapus untuk mencegah file corrupt tersisa di disk.
        """
        try:
            async with session.get(url, timeout=None) as response:
                response.raise_for_status()
                total_size = int(response.headers.get("Content-Length", 0))

                self.logger.info("Memulai proses pengunduhan...")

                progress_bar = None
                if self.show_progress:
                    progress_bar = tqdm(
                        total=total_size,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                        desc=os.path.basename(path)
                    )
                
                async with aiofiles.open(path, "wb") as f:
                    chunk_size = 8192
                    async for chunk in response.content.iter_chunked(chunk_size):
                        await f.write(chunk)
                        if progress_bar:
                            progress_bar.update(len(chunk))
                
                if progress_bar:
                    progress_bar.close()

                self.logger.info(f"\nUnduhan selesai! Video berhasil disimpan.")
        except aiohttp.ClientError as e:
            self.logger.error(f"Gagal mengunduh file: {e}")
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            self.logger.error(f"Terjadi kesalahan saat menyimpan file: {e}")
            if os.path.exists(path):
                os.remove(path)