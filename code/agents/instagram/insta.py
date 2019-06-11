import argparse
import os

import instaloader
import requests

IMAGES_PATH = "images"
FILE_PATTERN = "{date_utc}__{shortcode}"
# Get instance
loader = instaloader.Instaloader(download_comments=True, download_videos=False,
                                 download_video_thumbnails=False, compress_json=False,
                                 filename_pattern=FILE_PATTERN)


def send_to_server(hashtag, *, server):
    s = requests.Session()

    IMAGES_URL = f"http://{server}/api/{IMAGES_PATH}"

    for subdir, dirs, files in os.walk("#" + hashtag):
        only_pictures = [i for i in files if i.endswith(".jpg") or i.endswith(".png")]
        for pic in only_pictures:
            post_date, shortcode = pic.split("__")
            # removing the filename extension
            shortcode = shortcode[:-4]
            # check if the picture already exists
            resp = s.get(IMAGES_URL + "/search?short_code="+ shortcode)
            # If exists, ignore it
            if resp.status_code == requests.codes.ok:
                continue
            # if it doesn't exist, upload
            else:
                f = open(os.path.join(subdir,pic), "rb")
                s.post(url=IMAGES_URL + "?format=json", files={"file": f})
                f.close()
        break


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hashtag",
                        help="Hashtag to search for. Defaults to '#comidaportuguesa",
                        default=os.environ.get("HASHTAG", 'comidaportuguesa'))
    parser.add_argument("--limit",
                        help="Maximum number of results to search for. Defaults to 30",
                        default=int(os.environ.get("LIMIT", 30)),
                        type=int)
    parser.add_argument("--server_host",
                        help="Location of the server to connect to. Defaults to 127.0.0.1",
                        default=os.environ.get("SERVER_HOST", "127.0.0.1"))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    hashtag = args.hashtag
    limit = args.limit
    server = args.server_host
    # Download the posts
    loader.download_hashtag(hashtag=hashtag, max_count=limit,
                            post_filter=lambda post: post.is_video is False,
                            fast_update=True)
    # Send them to the server
    send_to_server(hashtag, server=server)
