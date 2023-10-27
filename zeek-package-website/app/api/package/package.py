import json
import os
from typing import Optional


def get_info(package_name: str) -> Optional[dict]:
    """
    Returns a dictionary of package information if package/json file exists.
    Returns None if the package does not exist

    Parameters
    ----------
    package_name : str
        The requested package name to find information for

    Returns
    -------
    dict
        A dictionary with the information about the package
    None
        None if no package with that name was found

    Examples
    --------
    >>> from app.api.package import package
    >>> name = "haash"
    >>> results = package.get_info(name)
    >>> print(results)
    """
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_files_dir = os.path.join(project_dir, "search", "json_files")
    document_names = os.listdir(json_files_dir)
    if package_name in document_names:
        json_file = open(os.path.join(json_files_dir, package_name), "r")
        json_data = json.loads(json_file.read())
        return json_data
    else:
        return None
