import json
import pathlib
from typing import (
    Dict,
    Optional,
    Union,
    Literal,
    List,
)

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
    """

    def __init__(
            self,
            storage_file: Optional[str] = None,
            data: Optional[Dict[str, Optional[Dict]]] = None,
        ) -> None:
        self.load(fp=storage_file)
        self.data = {} if data is None else data

    def add(self, obj: Dict[str, Optional[Dict]], parts: List[str]) -> None:
        """
        Adds the path parts to the object.

        Parameters:
        obj (dict): Object that will be edited.
        path (list): The listed parts of a path that will be added to the obj.
        """
        import datetime

        for part in parts:
            if part not in obj:
                obj[part] = {}
                # Defines the characteristics object.
                obj[part]["//"] = {}
            is_file = self.convert_to_path(parts).is_file()
            is_stored = part == parts[-1]
            features = obj[part]["//"]
            features["file"] = is_file
            features["stored"] = is_stored
            time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            features["stored_in"] = time if is_stored else None
            obj = obj[part]

    def remove_path(self, path: str) -> None:
        """
        Removes the managed path.

        Parameters:
        path (str): Path that will be removed.
        """
        path_obj = self.convert_to_path(path=path)
        self.rm(obj=self.data, path=path_obj.parts)

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

    def get_path(self, obj: Dict[str, Optional[Dict]]) -> str:
        """
        Returns the path of the past object.

        Parameters:
        obj (Dict[str, Optional[Dict]]): Object that will take the path.

        Returns:
        str: Path collected
        """
    def get_object(self, path: str) -> Dict[str, Optional[Dict]]:
        """
        Returns the path object.

        Parameters:
        path: Path that will be collected.

        Returns:
        Dict[str, Optional[Dict]]: Past path object.
        """
        obj = self.data
        path_obj = self.convert_to_path(path=path)
        for part in path_obj.parts:
            obj = obj[part]
        return obj

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
    def add_path(self, path: str) -> None:
        """
        Adds the path to the data.
        """
        path_obj = self.convert_to_path(path=path)
        self.add(obj=self.data, parts=path_obj.parts)

    def load(self, fp: str) -> None:
        """
        Loads a new path to be managed.

        Parameters:
        fp (str): File that will be managed.
        """
        with open(str(fp), "r") as file:
            new_data = json.load(file)
            self.set_data(data=new_data)

    def convert_to_path(self, path: Union[str, list]) -> pathlib.Path:
        """
        Returns the path instance of the 'pathlib.Path' class.

        Returns:
        pathlib.Path: Path instance.
        """
        path_class = pathlib.Path
        if isinstance(path, str):
            path_object = path_class(path)
        elif isinstance(path, list):
            path_object = path_class(*path)
        else:
            raise TypeError(f"The provided object must be a 'str' or 'list', the provided object was: {type(path).__name__}")
        if not path_object.exists():
            raise FileNotFoundError()
        return path_object

    def removes(self, paths: List[str]) -> None:
        """
        Removes the passed path if the path is in the data.

        Parameters:
        paths (List[str]): List of paths that will be removed.
        """
        for path in paths:
            self.remove(path)

    def rm(self, obj: Dict[str, Optional[dict]], parts: List[str]) -> None:
        """
        Removes the path object passed in a list.

        Parameters:
        obj (Dict[str, Optional[dict]]): Object for the path to be removed.
        path (list[str]): List of parts of a path.
        """
        if parts:
            for part in parts[:-1]:
                obj = obj[part]
            del obj[parts[-1]]

    def save(self) -> None:
        """
        Saves data to the storage file if the file is not None.
        """
        with open(self.storage_file, "w") as file:
            json.dump(self.data, file, indent=2)

    def set_data(self, data: Dict[str, Optional[dict]]) -> None:
        """
        Resets the managed data.

        Parameters:
        data: Dict[str, Optional[dict]]: Data that will be managed.
        """
        if not isinstance(data, dict):
            raise TypeError(f"The provided object must be a 'dict', the provided object was: {type(data).__name__}")
        setattr(self, "data", data)
