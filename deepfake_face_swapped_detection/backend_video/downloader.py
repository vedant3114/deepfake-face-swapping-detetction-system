"""
Video downloader module using yt-dlp
"""
import os
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
    
    # Output template
    output_template = os.path.join(output_dir, '%(id)s.%(ext)s')
    
    # yt-dlp options
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': output_template,
        'quiet': False,
        'no_warnings': False,
        'socket_timeout': timeout,
        'retries': 3,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info.get('id', 'video')
            ext = info.get('ext', 'mp4')
            downloaded_file = os.path.join(output_dir, f"{video_id}.{ext}")
            
            if os.path.exists(downloaded_file):
                return downloaded_file
            else:
                raise Exception(f"Downloaded file not found: {downloaded_file}")
                
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")
