import os
import uuid
import glob
import requests
import yt_dlp
import instaloader
from urllib.parse import urlparse

# Selenium stack for dynamic pages (Instagram/Reddit)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def _parse_srcset_for_highest_resolution(srcset: str) -> str:
    """
    Parse srcset attribute and return the URL with the highest width.
    srcset format: "url1 150w, url2 640w, url3 1080w"
    Returns the URL with the largest width.
    """
    if not srcset:
        return None
    
    candidates = []
    parts = [p.strip() for p in srcset.split(",") if p.strip()]
    
    for part in parts:
        tokens = part.split()
        if len(tokens) >= 2:
            url = tokens[0]
            width_str = tokens[1].replace("w", "")
            try:
                width = int(width_str)
                candidates.append((url, width))
            except ValueError:
                continue
    
    if candidates:
        # Sort by width descending and return highest resolution URL
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]
    
    return None


def _should_skip_image(img_element) -> bool:
    """
    Filter out unwanted images like avatars, icons, profile pictures.
    Returns True if image should be skipped.
    """
    try:
        # Check dimensions (avatars are typically small)
        width = img_element.size.get('width', 0)
        height = img_element.size.get('height', 0)
        if width < 200 or height < 200:
            return True
        
        # Check class names for common patterns
        class_name = (img_element.get_attribute("class") or "").lower()
        skip_classes = ["avatar", "profile", "icon", "logo", "button", "nav", "header"]
        if any(skip_class in class_name for skip_class in skip_classes):
            return True
        
        # Check alt text
        alt_text = (img_element.get_attribute("alt") or "").lower()
        skip_alts = ["profile picture", "avatar", "icon", "logo"]
        if any(skip_alt in alt_text for skip_alt in skip_alts):
            return True
        
        return False
    except Exception:
        return False


def _extract_og_image(driver) -> str:
    """
    Extract Open Graph image metadata from page.
    Returns the og:image URL or None.
    """
    try:
        og_meta = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:image"]')
        og_image_url = og_meta.get_attribute("content")
        if og_image_url and og_image_url.startswith("http"):
            print(f"Found OG image: {og_image_url}")
            return og_image_url
    except Exception as e:
        print(f"No OG image found: {e}")
    return None


def _extract_article_images(driver) -> list:
    """
    Extract images from <article> element (Instagram post container).
    Returns list of (url, estimated_quality_score) tuples.
    """
    candidates = []
    
    try:
        # Instagram wraps posts in <article> tags
        articles = driver.find_elements(By.TAG_NAME, "article")
        if not articles:
            print("No <article> elements found")
            return candidates
        
        # Use first article (main post)
        article = articles[0]
        imgs = article.find_elements(By.TAG_NAME, "img")
        print(f"Found {len(imgs)} images in article")
        
        for img in imgs:
            # Skip unwanted images
            if _should_skip_image(img):
                continue
            
            # Try to get highest resolution from srcset
            srcset = img.get_attribute("srcset") or ""
            highest_res_url = _parse_srcset_for_highest_resolution(srcset)
            
            if highest_res_url:
                # Estimate quality by URL (Instagram uses resolution in URL)
                quality_score = len(highest_res_url)  # Simple heuristic
                candidates.append((highest_res_url, quality_score))
            else:
                # Fallback to src attribute
                src = img.get_attribute("src")
                if src and src.startswith("http"):
                    candidates.append((src, 0))
        
    except Exception as e:
        print(f"Error extracting article images: {e}")
    
    return candidates


def fetch_image_via_selenium(url: str, output_dir: str, unique_id: str, timeout: int = 12) -> str:
    """
    Enhanced Instagram/Reddit image extraction using Selenium.
    
    Strategy:
    1. Try Open Graph metadata (og:image) - fastest & most reliable
    2. Fallback: Extract from <article> element with quality filtering
    3. Parse srcset for highest resolution
    4. Filter out avatars, icons, UI elements
    
    Returns the saved file path, or None on failure.
    """
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,720")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")

    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(timeout)
        driver.get(url)

        # Wait for page to render
        WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
        
        image_url = None
        
        # STRATEGY 1: Try Open Graph metadata (Instagram always has this)
        print("Trying OG metadata extraction...")
        image_url = _extract_og_image(driver)
        
        # STRATEGY 2: Fallback to article-scoped extraction
        if not image_url:
            print("OG metadata failed, trying article extraction...")
            candidates = _extract_article_images(driver)
            
            if candidates:
                # Sort by quality score (highest first)
                candidates.sort(key=lambda x: x[1], reverse=True)
                image_url = candidates[0][0]
                print(f"Selected best candidate: {image_url}")
            else:
                print("No suitable images found in article")
        
        if not image_url:
            print("Selenium: no usable image found")
            return None
        
        # Download the image
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = requests.get(image_url, headers=headers, stream=True, timeout=10)
        resp.raise_for_status()

        content_type = resp.headers.get("content-type", "")
        ext = ".jpg"
        if "png" in content_type:
            ext = ".png"
        if "webp" in content_type:
            ext = ".webp"

        final_path = os.path.join(output_dir, f"{unique_id}{ext}")
        with open(final_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        if os.path.getsize(final_path) > 0:
            print(f"Successfully downloaded image to: {final_path}")
            return final_path
        return None

    except Exception as e:
        print(f"Selenium strategy failed: {e}")
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

def get_instagram_shortcode(url: str) -> str:
    """Extracts the shortcode from an Instagram URL."""
    try:
        path = urlparse(url).path
        parts = [p for p in path.split('/') if p]
        if 'p' in parts:
            return parts[parts.index('p') + 1]
        elif 'reel' in parts:
            return parts[parts.index('reel') + 1]
        return None
    except:
        return None

def download_instagram_image(url: str, output_dir: str) -> str:
    """
    Downloads the image from an Instagram post using Instaloader.
    Returns the path to the downloaded image file.
    """
    shortcode = get_instagram_shortcode(url)
    if not shortcode:
        print("Could not extract Instagram shortcode.")
        return None

    L = instaloader.Instaloader(
        download_pictures=True,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False, 
        save_metadata=False,
        compress_json=False
    )
    
    # Target directory for this specific download
    target_dir = os.path.join(output_dir, shortcode)
    
    try:
        print(f"Attempting Instaloader download for {shortcode}...")
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=shortcode) # Downloads to 'shortcode' directory relative to cwd? 
        # Instaloader downloads to a directory named `target`. 
        # We need to control where that is. Instaloader uses cwd by default or `dirname_pattern`.
        
        # Actually Instaloader `download_post` 'target' argument is the directory name. 
        # But we want to ensure it goes into our output_dir.
        # Let's change cwd temporarily or move files? 
        # Better: Instaloader saves to {target}/{filename}.
        
        # We can simulate the download manually if needed, but let's try the library method.
        # If we pass target=os.path.join(output_dir, shortcode), it creates that dir.
        
        # Let's verify files.
        # Instaloader saves .jpg and .txt (if caption).
        
        # Workaround: Use a unique target name in the output_dir
        unique_target = os.path.join(output_dir, shortcode)
        L.download_post(post, target=unique_target)
        
        # Find the .jpg file
        files = glob.glob(os.path.join(unique_target, "*.jpg"))
        if files:
            return files[0]
        
        return None

    except Exception as e:
        print(f"Instaloader failed: {e}")
        return None

def download_image(url: str, output_dir: str = "tmp_downloads_images") -> str:
    """
    Main entry point for downloading images from various sources (Direct, Social).
    """
    os.makedirs(output_dir, exist_ok=True)
    unique_id = str(uuid.uuid4())

    # 0. Selenium Strategy (handles dynamic pages like Instagram/Reddit)
    print("Trying Selenium headless render for dynamic page...")
    selenium_path = fetch_image_via_selenium(url, output_dir, unique_id)
    if selenium_path:
        return selenium_path
    print("Selenium strategy did not yield an image; falling back.")
    
    # 1. Instagram Strategy
    if "instagram.com" in url:
        print("Detected Instagram URL, trying Instaloader...")
        # Instaloader is tricky with paths, let's try a dedicated subdir
        insta_path = download_instagram_image(url, output_dir)
        if insta_path:
            # Move/Rename to our standard unique_id in the main dir for consistency
            final_path = os.path.join(output_dir, f"{unique_id}.jpg")
            os.rename(insta_path, final_path)
            # Cleanup dir if empty? Instaloader leaves json/txt
            return final_path
        print("Instaloader failed, falling back to yt-dlp...")

    # 2. yt-dlp Strategy (Generic Social + Fallback)
    # We try to get the thumbnail or the image itself
    
    output_template = os.path.join(output_dir, f"{unique_id}.%(ext)s")
    
    # Strategy 2a: Try writing thumbnail (often the image for social posts)
    ydl_opts_thumb = {
        'outtmpl': output_template,
        'quiet': False,
        'writethumbnail': True,
        'skip_download': True, # We only want the "thumbnail" which is the image for posts
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts_thumb) as ydl:
            ydl.download([url])
            
        # Check for files
        files = glob.glob(os.path.join(output_dir, f"{unique_id}.*"))
        # yt-dlp might name it .jpg or .webp
        if files and os.path.getsize(files[0]) > 0:
            return files[0]
            
    except Exception as e:
        print(f"yt-dlp thumbnail strategy failed: {e}")

    # Strategy 2b: Full download (if it's a direct image link served via html wrapper?)
    # or just normal yt-dlp download if 2a failed
    ydl_opts_full = {
        'outtmpl': output_template,
        'quiet': False,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts_full) as ydl:
            ydl.download([url])
        
        files = glob.glob(os.path.join(output_dir, f"{unique_id}.*"))
        if files and os.path.getsize(files[0]) > 0:
            return files[0]
    except Exception as e:
        print(f"yt-dlp full download failed: {e}")

    # 3. Direct Request Strategy (Last Resort)
    try:
        print("Trying direct request...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, stream=True, timeout=10)
        resp.raise_for_status()
        
        content_type = resp.headers.get('content-type', '')
        ext = ".jpg"
        if "png" in content_type: ext = ".png"
        if "webp" in content_type: ext = ".webp"
        
        final_path = os.path.join(output_dir, f"{unique_id}{ext}")
        with open(final_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        
        if os.path.getsize(final_path) > 0:
            return final_path
            
    except Exception as e:
        print(f"Direct request failed: {e}")

    return None
