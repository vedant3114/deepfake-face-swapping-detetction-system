"""
Video downloader module using yt-dlp
"""
import os
import uuid
import glob
import yt_dlp



def get_video_metadata(url: str) -> dict:
    """
    Extract video metadata without downloading
    
    Args:
        url: Video URL
        
    Returns:
        dict: Video metadata
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title', 'Unknown'),
            'duration': info.get('duration', 0),
            'uploader': info.get('uploader', 'Unknown'),
            'format': info.get('format', 'Unknown'),
        }


def download_video(url: str, output_dir: str = "tmp_downloads", timeout: int = 120) -> str:
    """
    Download video from URL using yt-dlp
    
    Args:
        url: Video URL to download
        output_dir: Directory to save the downloaded video
        timeout: Download timeout in seconds
        
    Returns:
        str: Path to the downloaded video file
        
    Raises:
        Exception: If download fails
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert YouTube Shorts to regular YouTube URL for better compatibility
    if 'youtube.com/shorts/' in url:
        # Extract video ID from shorts URL
        import re
        match = re.search(r'shorts/([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1)
            url = f"https://www.youtube.com/watch?v={video_id}"
            print(f"Converted YouTube Shorts URL to: {url}")
    
    # Generate unique ID for this download (avoids filename collisions)
    unique_id = str(uuid.uuid4())
    output_template = os.path.join(output_dir, f"{unique_id}.%(ext)s")
    
    # yt-dlp options with improved compatibility
    ydl_opts = {
        'format': 'best[filesize<250M]/best',  # Limit file size to avoid timeout
        'outtmpl': output_template,
        'quiet': False,
        'no_warnings': False,
        'socket_timeout': timeout,
        'retries': 3,  # Simple integer for retry count
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        },
        'skip_unavailable_fragments': True,
        'fragment_retries': 10,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Attempting download to: {output_template}")
            print(f"URL: {url}")
            info = ydl.extract_info(url, download=True)
            
            # Find the file that was just created starting with unique_id
            # This handles cases where ext might change (mkv, webm, mp4)
            found_files = glob.glob(os.path.join(output_dir, f"{unique_id}.*"))
            
            if found_files:
                final_path = found_files[0]
                file_size = os.path.getsize(final_path)
                print(f"File size: {file_size} bytes")
                
                # Verify file size > 0
                if file_size > 0:
                    print(f"✓ Download successful: {final_path}")
                    return final_path
                else:
                    os.remove(final_path)
                    raise Exception("Downloaded file is empty (0 bytes). YouTube may be blocking the request.")
            
            raise Exception("yt-dlp finished but no file found matching pattern.")
                
    except Exception as e:
        print(f"❌ Download Error: {e}")
        # Clean up any partial files
        partial_files = glob.glob(os.path.join(output_dir, f"{unique_id}.*"))
        for f in partial_files:
            try:
                os.remove(f)
            except:
                pass
        raise Exception(f"Failed to download video: {str(e)}")

