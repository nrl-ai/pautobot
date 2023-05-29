import pkg_resources
import os
import shutil
import pathlib


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
