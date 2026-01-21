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
    
    # Generate unique ID for this download (avoids filename collisions)
    unique_id = str(uuid.uuid4())
    output_template = os.path.join(output_dir, f"{unique_id}.%(ext)s")
    
    # yt-dlp options
    ydl_opts = {
        'format': 'best', # Let yt-dlp choose best quality, we'll handle conversion if needed
        'outtmpl': output_template,
        'quiet': False,
        'no_warnings': False,
        'socket_timeout': timeout,
        'retries': 3,
        # 'noplaylist': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Attempting download to: {output_template}")
            info = ydl.extract_info(url, download=True)
            
            # Find the file that was just created starting with unique_id
            # This handles cases where ext might change (mkv, webm, mp4)
            found_files = glob.glob(os.path.join(output_dir, f"{unique_id}.*"))
            
            if found_files:
                final_path = found_files[0]
                # Verify file size > 0
                if os.path.getsize(final_path) > 0:
                    print(f"Download successful: {final_path}")
                    return final_path
                else:
                    os.remove(final_path)
                    raise Exception("Downloaded file is empty (0 bytes).")
            
            raise Exception("yt-dlp finished but no file found matching pattern.")
                
    except Exception as e:
        print(f"Download Error: {e}")
        raise Exception(f"Failed to download video: {str(e)}")

