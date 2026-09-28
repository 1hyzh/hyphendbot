from typing import Any, Dict, Optional

DEFAULT_LASTFM_IMAGE_HASH = '2a96cbd8b46e442fc41c2b86b821562f'


def get_album_image(track: Dict[str, Any]) -> Optional[str]:
    images = track.get('image', [])
    for image in reversed(images):
        url = image.get('#text', '').strip()
        if url and DEFAULT_LASTFM_IMAGE_HASH not in url:
            return url
    return None


def get_full_quality_image(track: Dict[str, Any]) -> Optional[str]:
    image_url = get_album_image(track)
    if image_url is None:
        return None
    return image_url.replace('/300x300/', '/770x0/')


def get_rpc_image(track: Dict[str, Any]) -> Optional[str]:
    return get_full_quality_image(track)


def get_album_name(track: Dict[str, Any]) -> str:
    album = track.get('album', {})
    return album.get('#text', '').strip()
