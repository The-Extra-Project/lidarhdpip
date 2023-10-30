"""
here we store the various standards of data inputs/outputs that are being processed by the various jobs
"""
from typing import List

class surface_reconstruction_pipeline:
    coordinates: List[str]
    laz_file: str
    username:str
    template_file: str
    filename_pipeline: str
    surface_reconstruction_algorithm: str

class citygml_pipeline:
    yaml_file_path: str
    object_file_path: str
    cityGML_output_path:str    