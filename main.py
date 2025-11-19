import os
import random
import pytz
import tweepy
import logging
import cloudscraper
from datetime import datetime

# -----------------------------
# AYARLAR
# -----------------------------
IMAGE_DIR = "src"
FIXED_LINK = os.getenv("FIXED_LINK")

# -----------------------------
# TWITTER API
# -----------------------------
twitter_client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
    wait_on_rate_limit=True
)

# -----------------------------
# NEXTSOSYAL API
# -----------------------------
NEXTSOSYAL_TOKEN = os.getenv("NEXT_ACCESS_TOKEN")
if not NEXTSOSYAL_TOKEN:
    raise ValueError("NextSosyal token bulunamadı! 'NEXT_ACCESS_TOKEN' tanımlayın.")

NEXTSOSYAL_BASE_URL = "https://sosyal.teknofest.app"
scraper = cloudscraper.create_scraper(
    browser={'custom': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/115.0.0.0 Safari/537.36'}
)

# -----------------------------
# LOGGING
# -----------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -----------------------------
# FONKSİYONLAR
# -----------------------------
def pick_random_image(image_dir: str) -> str | None:
    files = [f for f in os.listdir(image_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not files:
        logging.error(f"[Resim Seçimi] Hiç resim bulunamadı: {image_dir}")
        return None
    chosen = random.choice(files)
    logging.info(f"[Resim Seçimi] Seçilen resim: {chosen}")
    return os.path.join(image_dir, chosen)

def upload_media_twitter(file_path: str) -> str | None:
    if not os.path.exists(file_path):
        logging.error(f"[Twitter] Medya bulunamadı: {file_path}")
        return None
    api = tweepy.API(tweepy.OAuth1UserHandler(
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_SECRET"),
        os.getenv("TWITTER_ACCESS_TOKEN"),
        os.getenv("TWITTER_ACCESS_SECRET")
    ))
    media = api.media_upload(file_path)
    logging.info(f"[Twitter] Medya yüklendi: {media.media_id_string}")
    return media.media_id_string

def send_twitter(text: str, media_id: str | None = None):
    twitter_client.create_tweet(text=text, media_ids=[media_id] if media_id else None)
    logging.info("[Twitter] Gönderildi.")

def upload_media_nextsosyal(file_path: str) -> str | None:
    if not os.path.exists(file_path):
        logging.error(f"[NextSosyal] Medya bulunamadı: {file_path}")
        return None
    url = f"{NEXTSOSYAL_BASE_URL}/api/v1/media"
    headers = {"Authorization": f"Bearer {NEXTSOSYAL_TOKEN}"}
    with open(file_path, "rb") as f:
        response = scraper.post(url, headers=headers, files={"file": f})
    if response.status_code == 200:
        media_id = response.json().get("id")
        logging.info(f"[NextSosyal] Medya yüklendi: {media_id}")
        return media_id
    logging.error(f"[NextSosyal] Medya yükleme hatası {response.status_code}: {response.text}")
    return None

def send_nextsosyal(text: str, media_id: str | None = None):
    url = f"{NEXTSOSYAL_BASE_URL}/api/v1/statuses"
    headers = {"Authorization": f"Bearer {NEXTSOSYAL_TOKEN}"}
    data = [("status", text), ("visibility", "public")]
    if media_id:
        data.append(("media_ids[]", str(media_id)))
    response = scraper.post(url, headers=headers, data=data)
    if response.status_code == 200:
        logging.info("[NextSosyal] Gönderildi.")
    else:
        logging.error(f"[NextSosyal] Gönderilemedi {response.status_code}: {response.text}")

# -----------------------------
# MAIN
# -----------------------------
def main():
    image_path = pick_random_image(IMAGE_DIR)
    if not image_path:
        return

    tz = pytz.timezone("Europe/Istanbul")
    text = f"🧭 Pusula\n📅 {datetime.now(tz):%d.%m.%Y} itibariyle güncellenmiştir.\n🔗 {FIXED_LINK}"

    # --- Twitter ---
    twitter_media_id = upload_media_twitter(image_path)
    send_twitter(text, twitter_media_id)

    # --- NextSosyal ---
    next_media_id = upload_media_nextsosyal(image_path)
    send_nextsosyal(text, next_media_id)

# -----------------------------
if __name__ == "__main__":
    main()
