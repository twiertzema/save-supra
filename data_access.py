import json
import os
import re

from typing import Dict, List, NewType, Optional

SUPRA_ID = "UC6iBH7Pmiinoe902-JqQ7aQ"

BVGM_PLAYLIST_IDS = (
    "PL9B23A78D3D249A74",  # 1
    "PLF10B9FEF959D8065",  # 2
    "PLB45265BFFA7BE793",  # 3
    "PL632918E68D9E576A",  # 4
    "PL16375BD0AA7CB9B9",  # 5
    "PL3A5F5309568FEB54",  # 6
    "PLz2Bd4VjE_0WzuZ8MhtJVnht77NSirtwR",  # 7
    "PLz2Bd4VjE_0VhYCcUKF8mcOkYXVVUyBMI",  # 8
    "PLz2Bd4VjE_0WdSywD9jjN132_0YME_psr",  # 9
    "PLz2Bd4VjE_0Vw55wuTq7ine06pDKnkMC5",  # 10
    "PLz2Bd4VjE_0UiEAFkiEABy9SQt1WPdp1_",  # 11
    "PLz2Bd4VjE_0WLmOKFO1DEogbIGIp3PzRU",  # 12
    "PLz2Bd4VjE_0Wuw9TuOipbZtx7vQNCgB-Q",  # 13
)
OTHER_PLAYLIST_IDS = (
    "PLz2Bd4VjE_0WTtp7zh-kNqnbcPxVMXUZE",
    "PLz2Bd4VjE_0Xhvmx4l_XcsZ16AvpgBb0q",
    "PLz2Bd4VjE_0Xt4GMfbCll_Xt2o_QJl3T9",
    "PLz2Bd4VjE_0Uuo5qDjgwpdbj1pUMwhXu0",
    "PL719789CCE8C818B5",
    "PLC28D927FFE1F659B",
    "PL7565A9718D6CEBA3",
    "PL0FBC75AC445137EC",
    "PL518CB8785D7478E4",
    "PL34FAB428055ED1D3",
)

ROOT_DIR = os.path.join(os.getcwd(), "db")

BVGM_NUM_REGEX = re.compile(r"^.*Best VGM (\d+).*")


class DataAccess:
    def __init__(self, root_dir: Optional[str] = None):
        self.root_dir = root_dir or os.getcwd()
        self.db_dir = os.path.join(self.root_dir, "db")

    @staticmethod
    def __get_json(abs_file_path: str):
        with open(abs_file_path, mode="r", encoding="utf-8") as f:
            raw_data = f.read()
            result = json.loads(raw_data)

        return result

    @staticmethod
    def __get_bvgm_number(video):
        title = video["snippet"]["title"]
        return int(re.match(BVGM_NUM_REGEX, title).group(1))

    def get_playlists(self, ids: List[str] = None):
        result = []
        for root, dirs, files in os.walk(os.path.join(self.db_dir, "playlists")):
            for filename in files:
                pid = filename.split(".")[0]

                # Skip if not in the desired set.
                if ids and pid not in ids:
                    continue

                playlist = self.__get_json(f"{root}\\{filename}")
                result.append(playlist)
        return result

    def get_pitems_dict(self):
        pitems_ids = []
        for root, dirs, files in os.walk(os.path.join(self.db_dir, "playlist_items")):
            pitems_ids = [filename.split(".")[0] for filename in files]

        result = {}
        for root, dirs, files in os.walk(os.path.join(self.db_dir, "playlists")):
            for filename in files:
                playlist_id = filename.split(".")[0]

                if playlist_id not in pitems_ids:
                    # Don't have playlist items for this playlist.
                    continue

                result[playlist_id] = self.get_playlist_items(playlist_id)

        return result

    def get_playlist_items(self, playlist_id: str):
        return self.__get_json(
            os.path.join(self.db_dir, "playlist_items", f"{playlist_id}.json")
        )

    def get_videos_dict(self, playlist_ids: str):
        result = {}
        for pid in playlist_ids:
            videos = self.get_videos_for_playlist(pid)
            result[pid] = videos

        return result

    def get_videos_for_playlist(self, playlist_id: str):
        playlist_items = self.get_playlist_items(playlist_id)

        result = []
        for item in playlist_items:
            vid = item["contentDetails"]["videoId"]
            try:
                video = self.get_video(vid)
                result.append(video)
            except FileNotFoundError:
                print(f"Couldn't find video: {vid}")

        return result

    def get_all_videos(self, sort: bool = False):
        for root, dirs, files in os.walk(os.path.join(self.db_dir, "videos")):
            videos = []

            for filename in files:
                video = self.__get_json(f"{root}\\{filename}")
                videos.append(video)

            if sort:
                videos.sort(key=lambda item: self.__get_bvgm_number(item))

            return videos

    def get_video(self, vid: str):
        return self.__get_json(os.path.join(self.db_dir, "videos", f"{vid}.json"))

    def get_threads_for_video(self, vid: str):
        return self.__get_json(
            os.path.join(self.db_dir, "commentThreads", f"{vid}.json")
        )

    def have_comments_for_video(self, vid: str):
        return os.path.exists(
            os.path.join(self.db_dir, "commentThreads", f"{vid}.json")
        )
