import os
import uuid
import glob
import requests
import yt_dlp
import instaloader
from urllib.parse import urlparse

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
