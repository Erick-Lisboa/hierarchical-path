import json
import pathlib
from typing import Dict, Optional, Union, Literal, List

class PathManager:
    """
    Hierarchically stored valid path data manager.
    The hierarchy is an object with nested paths, where each part of the
    path has its characteristics stored in a key represented by "//".
    Itscharacteristics are as follows:
        "stored", if part of the path was stored;
        "file", if the path is a file;
        "stored_in", when it was stored;

    Parameters:
    -----------
    data: Opitional[dict]
        Data that will be managed.
    storage_file: Opitioal[str]
        Path of the .json file that will store and read the data for management

    Attributes:
    -----------
    data: dict
        Hierarchical path storage data.
    storage_file: str
        Path of the .json file that will store the data
    """

    def __init__(
            self,
            data: Optional[Dict[str, Optional[Dict]]] = None,
            storage_file: Optional[str] = None,
        ) -> None:
        self.path: pathlib.Path
        self.data = {} if data is None else data
        self.storage_file = storage_file

    def add(self, segment: Dict[str, Optional[Dict]], parts: List[str]) -> None:
        """
        Adds the path parts to the segment.

        Parameters:
        segment (dict): Segment that will be edited.
        path (list): The listed parts of a path that will be added to the segment.
        """
        import datetime

        for part in parts:
            if part not in segment:
                segment[part] = {}
                segment[part]["//"] = {}  # Defines the characteristics object.
            is_file = self.path.is_file()
            is_stored = part == parts[-1]
            features = segment[part]["//"]
            features["file"] = is_file
            features["stored"] = is_stored
            time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            features["stored_in"] = time if is_stored else None
            segment = segment[part]

    def decrease(self, path: str) -> None:
        """
        Removes the managed path.

        Parameters:
        path (str): Path that will be removed.
        """
        setattr(self, "path", self.convert_to_path(path=path))
        self.rm(segment=self.data, path=self.path.parts)
        self.path = None

    def find(self, path: str) -> Dict[str, Optional[Dict]]:
        """               
        Returns the segment of the past path.

        Parameters:
        path (str): Path that will be searched.

        Returns:
        dict (Dict[str, Optional[Dict]]): Segment of the past path sought.
        """
        segment = self.data
        path_obj = self.convert_to_path(path=path)
        for part in path_obj.parts:
            segment = segment[part]
        return segment

    def get_all(self) -> Optional[List[str]]:
        """
        Returns all stored paths.

        Returns:
        List[str]: All stored paths.
        None: If there is no data stored.
        """
    def get_data(self) -> Dict[str, Optional[Dict]]:
        """
        Get the current data.
        """
        return getattr(self, "data")

    def get_path(self, segment: Dict[str, Optional[Dict]]) -> str:
        """
        Returns the path of the past segment.

        Parameters:
        segment (Dict[str, Optional[Dict]]): Segment that will take the path.

        Returns:
        str: Path collected
        """
    def get_segment(self, path: str) -> Dict[str, Optional[Dict]]:
        """
        Returns the path segment.

        Parameters:
        path: Path that will be collected.

        Returns:
        Dict[str, Optional[Dict]]: Past path segment.
        """
    def get_stored(self) -> Optional[Dict[str, Optional[Dict]]]:
        """
        Returns the stored data if there is a file.

        Returns:
        Dict[str, Optional[Dict]]: Stored data.
        None: If there is no data stored.
        """
    def in_the_data(self, path: str) -> bool:
        """
        Returns whether the path is.

        Returns:
        bool: If the path is stored.
        """
    def increase(self, path: str) -> None:
        """
        Adds the path to the data.
        """
        setattr(self, "path", self.convert_to_path(path=path))
        self.add(segment=self.data, path=self.path.parts)
        setattr(self, "path", None)

    def upload_current_storage(self) -> None:
        """
        Loads the storage file and sets data as its content.
        """
        self.upload(self.storage_file)

    def upload_new_storage(self, storage_file: str) -> None:
        """
        Resets the managed data to the contents of the .json file.

        Parameters:
        storage_file (str): File that will be loaded and managed.
        """
        self.upload(storage_file)

    def upload(self, storage_file: str) -> None:
        """
        Loads a new path to be managed.

        Parameters:
        storage_file (str): File that will be managed.
        """
        with open(str(storage_file), "r") as file:
            new_data = json.load(file)
            setattr(self, "data", new_data)

    def convert_to_path(self, path: str) -> pathlib.Path:
        """
        Returns the path instance of the 'pathlib.Path' class.

        Returns:
        pathlib.Path: Path instance.
        """
        if not isinstance(path, str):
            raise TypeError(f"The provided object must be a 'str', the provided object was: {type(path).__name__}")
        path_object = pathlib.Path(path)
        if not path_object.exists():
            raise FileNotFoundError()
        return path_object

    def remove(self, path: str) -> None:
        """
        Removes the past path.

        Parameters:
        path (str): Path that will be removed
        """
        if isinstance(path, str):
            path = self.convert_to_path(path)

        self.rm(segment=self.data, path=path.parts)

    def removes(self, paths: List[str]) -> None:
        """
        Removes the passed path if the path is in the data.

        Parameters:
        paths (List[str]): List of paths that will be removed.
        """
        for path in paths:
            self.remove(path)

    def remove_file(self) -> None:
        """
        Removes the file from storage. Sets the 'data' attribute to None. 
        """
        setattr(self, "storage_file", None)

    def rm(self, segment: Dict[str, Optional[dict]], parts: List[str]) -> None:
        """
        Removes the path segment passed in a list.

        Parameters:
        segment (Dict[str, Optional[dict]]): Segment for the path to be removed.
        path (list[str]): List of parts of a path.
        """
        for part in parts[:-1]:
            segment = segment[part]
        segment.clear()

    def save(self) -> None:
        """
        Saves data to the storage file if the file is not None.
        """
        with open(self.storage_file, "w") as file:
            json.dumps(file)

    def set_data(self, data: Dict[str, Optional[dict]]) -> None:
        """
        Resets the managed data.

        Parameters:
        data: Dict[str, Optional[dict]]: Data that will be managed.
        """
        if not isinstance(data, dict):
            raise TypeError(f"The provided object must be a 'dict', the provided object was: {type(data).__name__}")
        setattr(self, "data", data)

    def set_file(self, path: Optional[str]) -> None:
        """
        Defines the storage file, the 'data' attribute is changed to the file data and the data will be saved in the file.

        Parameters:
        path (Opitional[str]): The storage file.
        """
        setattr(self, "storage_file", path)
