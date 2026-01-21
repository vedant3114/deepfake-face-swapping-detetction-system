import re
import logging

logger = logging.getLogger(__name__)

# Platform patterns for robust detection
PLATFORM_PATTERNS = {
    "youtube": [
        r"(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)",
        r"(?:youtube\.com/watch\?v=|youtu\.be/)"
    ],
    "instagram": [
        r"(?:https?://)?(?:www\.)?instagram\.com",
        r"(?:instagram\.com/p/|instagram\.com/reel/)",
    ],
    "facebook": [
        r"(?:https?://)?(?:www\.)?(?:facebook\.com|fb\.com)",
        r"(?:facebook\.com/(?:video|watch))",
    ],
    "tiktok": [
        r"(?:https?://)?(?:www\.)?tiktok\.com",
        r"(?:tiktok\.com/@.*?/video/)",
    ],
    "twitter": [
        r"(?:https?://)?(?:www\.)?(?:twitter\.com|x\.com)",
        r"(?:twitter\.com|x\.com)/\w+/status/",
    ],
    "direct": [
        r"\.mp4$",
        r"\.webm$",
        r"\.mkv$",
        r"\.mov$",
        r"\.avi$",
    ]
}

def detect_platform(url: str) -> str:
    """
    Detects video platform from URL.
    Supports: YouTube, Instagram, Facebook, TikTok, Twitter/X, and direct URLs
    
    Args:
        url: Video URL
        
    Returns:
        str: Platform name (youtube, instagram, facebook, tiktok, twitter, direct, or unknown)
    """
    url = url.lower().strip()
    
    for platform, patterns in PLATFORM_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, url):
                logger.info(f"Detected platform: {platform}")
                return platform
    
    logger.warning(f"Unknown platform for URL: {url}")
    return "unknown"


def is_supported_platform(platform: str) -> bool:
    """
    Check if platform is supported for video download.
    
    Args:
        platform: Platform name
        
    Returns:
        bool: True if platform is supported
    """
    supported = {
        "youtube": True,
        "instagram": True,
        "facebook": True,
        "tiktok": True,
        "twitter": True,
        "direct": True,
    }
    return supported.get(platform, False)


def get_platform_info(platform: str) -> dict:
    """
    Get information about a platform for UI display.
    
    Args:
        platform: Platform name
        
    Returns:
        dict: Platform info (name, icon, color, etc.)
    """
    info = {
        "youtube": {
            "name": "YouTube",
            "icon": "fab fa-youtube",
            "color": "#FF0000",
            "description": "Support for YouTube videos"
        },
        "instagram": {
            "name": "Instagram",
            "icon": "fab fa-instagram",
            "color": "#E4405F",
            "description": "Support for Instagram posts and reels"
        },
        "facebook": {
            "name": "Facebook",
            "icon": "fab fa-facebook",
            "color": "#1877F2",
            "description": "Support for Facebook videos"
        },
        "tiktok": {
            "name": "TikTok",
            "icon": "fab fa-tiktok",
            "color": "#000000",
            "description": "Support for TikTok videos"
        },
        "twitter": {
            "name": "Twitter / X",
            "icon": "fab fa-twitter",
            "color": "#000000",
            "description": "Support for Twitter/X videos"
        },
        "direct": {
            "name": "Direct URL",
            "icon": "fas fa-link",
            "color": "#0066CC",
            "description": "Direct MP4/WebM file URLs"
        }
    }
    return info.get(platform, {
        "name": platform.capitalize(),
        "icon": "fas fa-video",
        "color": "#666666",
        "description": f"Support for {platform} videos"
    })

