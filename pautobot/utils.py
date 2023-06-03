import pkg_resources
import os
import shutil
import pathlib
import traceback
import requests
import platform
import subprocess

import tempfile
from tqdm import tqdm


def open_file(path):
    """
    Open file in default application
    """
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def extract_frontend_dist(static_folder):
    """
    Extract folder frontend/dist from package pautobot
    and put it in the same static folder for serving
    """
    dist_folder = pkg_resources.resource_filename("pautobot", "frontend-dist")
    if os.path.exists(static_folder):
        shutil.rmtree(static_folder)
    pathlib.Path(static_folder).parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(dist_folder, static_folder)


def download_file(url, file_path):
    """
    Send a GET request to the URL
    """
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    pathlib.Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        total_size = int(response.headers.get("content-length", 0))
        block_size = 8192  # Chunk size in bytes
        progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

        with open(tmp_file.name, "wb") as file:
            # Iterate over the response content in chunks
            for chunk in response.iter_content(chunk_size=block_size):
                file.write(chunk)
                progress_bar.update(len(chunk))

        progress_bar.close()
        shutil.move(tmp_file.name, file_path)
        print("File downloaded successfully.")
    else:
        print("Failed to download file.")


def download_model(model_type, model_path):
    """
    Download model if not exists
    TODO (vietanhdev):
        - Support more model types
        - Multiple download links
        - Check hash of the downloaded file
    """
    MODEL_URL = "https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin"
    if not os.path.exists(model_path):
        print("Downloading model...")
        try:
            download_file(MODEL_URL, model_path)
        except Exception as e:
            print(f"Error while downloading model: {e}")
            traceback.print_exc()
            exit(1)
        print("Model downloaded!")
