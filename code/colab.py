# ==================== CONFIGURATION ====================
HDFS_HOST = "160.191.162.36"
WEBHDFS_PORT = 9870
HDFS_BASE_PATH = "/user/pickles"  # No trailing slash
FILES_TO_FETCH = ["video_chunk_10.pkl.xz", "video_chunk_50.pkl.xz"]

LOCAL_DOWNLOAD_DIR = '/content/hdfs_files'

MAX_PARALLEL_JOBS = 8
# ====================================================================

import os
import requests
import concurrent.futures
import lzma
import pickle
os.makedirs(LOCAL_DOWNLOAD_DIR, exist_ok=True)

def download_file(file_name):
    url = f"http://{HDFS_HOST}:{WEBHDFS_PORT}/webhdfs/v1{HDFS_BASE_PATH}/{file_name}?op=OPEN&user.name=hdfs"
    local_path = os.path.join(LOCAL_DOWNLOAD_DIR, file_name)

    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_path
    except Exception as e:
        print(f"Error downloading {file_name}: {e}")
        return None

def decompress_and_load_xz_pickle(file_path):
    try:
        with lzma.open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Failed to load {file_path}: {e}")
        return None

# ------------------ DOWNLOAD IN PARALLEL ------------------
with concurrent.futures.ThreadPoolExecutor() as executor:
    downloaded_files = list(executor.map(download_file, FILES_TO_FETCH))
    downloaded_files = [f for f in downloaded_files if f]

# ------------------ DECOMPRESS AND LOAD PARALLEL ------------------
with concurrent.futures.ThreadPoolExecutor() as executor:
    loaded_objects = list(executor.map(decompress_and_load_xz_pickle, downloaded_files))

# You now have the uncompressed pickle objects in `loaded_objects`
for i, obj in enumerate(loaded_objects):
    print(f"\n--- Object {i+1} ---\n", obj)