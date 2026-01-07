import re
from typing import Dict

INSTAGRAM_POST_REGEX = re.compile(
    r"(https?://)?(www\.)?instagram\.com/(p|reel)/([A-Za-z0-9_-]+)"
)


def parse_instagram_url(url) -> Dict:
    """
    Validate Instagram URL and extract metadata.
    Accepts str or Pydantic HttpUrl.
    """

    # 🔴 FIX 1: Ensure URL is always a string
    url = str(url)

    # 🔴 FIX 2: Remove query parameters (?utm_source=...)
    clean_url = url.split("?")[0]

    # 🔴 FIX 3: Use search() instead of match()
    match = INSTAGRAM_POST_REGEX.search(clean_url)

    if not match:
        raise ValueError("Invalid Instagram post or reel URL")

    content_type = match.group(3)   # p or reel
    shortcode = match.group(4)

    return {
        "platform": "instagram",
        "content_type": "reel" if content_type == "reel" else "post",
        "shortcode": shortcode,
        "original_url": clean_url
    }
