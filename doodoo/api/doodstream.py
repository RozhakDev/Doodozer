import logging
import re
import random
import time
from typing import Optional, Tuple
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup

class DoodStreamAPI:
    """Kelas untuk berinteraksi dengan DoodStream API.

    Kelas ini menyediakan metode untuk mengakses dan memproses video dari platform
    DoodStream, termasuk mendapatkan URL unduhan langsung dan judul video.

    Attributes:
        session (aiohttp.ClientSession): Session HTTP untuk melakukan request.
        logger (logging.Logger): Logger untuk logging aktivitas kelas.
    """

    def __init__(self, session: aiohttp.ClientSession):
        """Menginisialisasi instance DoodStreamAPI.

        Args:
            session (aiohttp.ClientSession): Session HTTP yang digunakan untuk melakukan
                request ke DoodStream API.

        Raises:
            ValueError: Jika session yang diberikan bukan instance aiohttp.ClientSession.
        """
        self.session = session
        self.logger = logging.getLogger(__name__)
    
    async def get_download_url(self, url: str) -> Optional[Tuple[str, str]]:
        """Mendapatkan direct download URL dan judul video dari halaman DoodStream.

        Metode ini memproses halaman embed DoodStream untuk mengekstrak URL unduhan
        langsung dan judul video yang dapat digunakan untuk mengunduh video.

        Args:
            url (str): URL video DoodStream (contoh: https://dood.la/e/xxxxxxxx).
                       URL harus dalam format embed yang valid.

        Returns:
            Optional[Tuple[str, str]]: Tuple berisi (direct_download_url, title) jika berhasil,
                                     atau None jika gagal memproses URL.

        Raises:
            aiohttp.ClientError: Jika terjadi kesalahan saat melakukan request HTTP.
            Exception: Kesalahan umum lainnya yang terjadi saat memproses halaman.

        Contoh:
            >>> api = DoodStreamAPI(session)
            >>> download_url, title = await api.get_download_url("https://dood.la/e/xxxxxxxx")
            >>> if download_url:
            ...     print(f"Judul: {title}")
            ...     print(f"URL unduhan: {download_url}")
        """
        self.logger.info(f"Memproses URL: {url}")

        embed_url = url.replace('/d/', '/e/')

        try:
            self.session.headers.update({"Referer": embed_url})

            async with self.session.get(embed_url) as response:
                response.raise_for_status()
                html_content = await response.text()
            
            pass_md5_match = re.search(r'/pass_md5/([^"\']+)', html_content)
            if not pass_md5_match:
                self.logger.error("Tidak dapat menemukan 'pass_md5' pada halaman embed.")
                return None
            
            pass_md5_path = pass_md5_match.group(1)
            domain = urlparse(embed_url).netloc
            pass_md5_url = f"https://{domain}/pass_md5/{pass_md5_path}"
            self.logger.debug(f"URL pass_md5 ditemukan: {pass_md5_url}")

            async with self.session.get(pass_md5_url) as md5_response:
                md5_response.raise_for_status()
                media_url_base = await md5_response.text()

            token = pass_md5_path.split('/')[-1]
            random_chars = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=10))

            final_url = f"{media_url_base}{random_chars}?token={token}&expiry={int(time.time())}"

            soup = BeautifulSoup(html_content, "html.parser")
            title_tag = soup.find("title")
            title = title_tag.text.strip() if title_tag else token

            title = re.sub(r'[\\/*?:"<>|]', "", title)

            self.logger.info(f"Direct download link berhasil dibuat untuk '{title}'")
            return final_url, title
        except aiohttp.ClientError as e:
            self.logger.error(f"Request error saat mengakses DoodStream: {e}")
        except Exception as e:
            self.logger.error(f"Terjadi kesalahan saat memproses URL DoodStream: {e}", exc_info=True)

        return None