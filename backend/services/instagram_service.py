import re
from typing import Dict


INSTAGRAM_POST_REGEX = re.compile(
    r"(https?://)?(www\.)?instagram\.com/(p|reel)/([A-Za-z0-9_-]+)"
)


def parse_instagram_url(url: str) -> Dict:
    """
    Validate Instagram URL and extract metadata.
    """

    match = INSTAGRAM_POST_REGEX.match(url)

    if not match:
        raise ValueError("Invalid Instagram post or reel URL")

    content_type = match.group(3)   # p or reel
    shortcode = match.group(4)

    return {
        "platform": "instagram",
        "content_type": "reel" if content_type == "reel" else "post",
        "shortcode": shortcode,
        "original_url": url
    }
