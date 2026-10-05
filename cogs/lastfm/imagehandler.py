from typing import Any, Dict, Optional

DEFAULT_LASTFM_IMAGE_HASH = '2a96cbd8b46e442fc41c2b86b821562f' # last.fm default image hash


def get_album_image(track: Dict[str, Any]) -> Optional[str]: # pass the current track to get the cover art 
    images = track.get('image', [])
    for image in reversed(images):
        url = image.get('#text', '').strip()
        if url and DEFAULT_LASTFM_IMAGE_HASH not in url:
            return url
    return None


def get_full_quality_image(track: Dict[str, Any]) -> Optional[str]: # get the full quality cover for the >cover cmd
    image_url = get_album_image(track)
    if image_url is None:
        return None
    return image_url.replace('/300x300/', '/770x0/')


def get_rpc_image(track: Dict[str, Any]) -> Optional[str]: # get the cover art for the rpc presence
    return get_full_quality_image(track)


def get_album_name(track: Dict[str, Any]) -> str: # get the album name from the track data
    album = track.get('album', {})
    return album.get('#text', '').strip()
