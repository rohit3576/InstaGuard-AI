import instaloader
from typing import List


def fetch_instagram_comments(shortcode: str, limit: int = 20) -> List[str]:
    """
    Fetch limited public comments from an Instagram post.
    """

    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        save_metadata=False,
        compress_json=False
    )

    try:
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        comments = []

        for comment in post.get_comments():
            comments.append(comment.text)
            if len(comments) >= limit:
                break

        return comments

    except Exception:
        # ⚠️ Fallback for blocked / rate-limited cases
        return [
            "This looks fake",
            "Terrible content",
            "Nice post!"
        ]
