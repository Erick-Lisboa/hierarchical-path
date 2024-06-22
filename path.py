import json
import pathlib
from typing import (
    Dict,
    Optional,
    Union,
    Literal,
    List,
    Tuple,
)

msg = {
    "type_error": "The provided object must be a :class:`{}`, the provided object was: :class:`{}`"
}

class PathManager:
    """
    Hierarchically stored valid path data manager.
    The hierarchy is an object with nested paths, where each part of the
    path has its property stored in a key represented by "//".
    Its property are as follows:
        "stored", if part of the path was stored;
        "file", if the path is a file;
        "stored_in", when it was stored;

    Parameters:
    -----------
    data: Opitional[dict]
        Data that will be managed. Defaults to None.
    storage_file: Opitioal[str]
        Path of the .json file that will store and read the data for management. Defaults to None.

    Attributes:
    -----------
    data: dict
        Hierarchical path storage data.
    path_properties: dict
        Paths property object.
    """

    def __init__(
            self,
            storage_file: Optional[str] = None,
            data: Optional[Dict[str, Optional[Dict]]] = None,
        ) -> None:
        if storage_file is not None:
            self.load(fp=storage_file)
        else:
            self.data = {} if data is None else data
        self.path_properties = {"file": False, "stored": False, "stored_in": None}

    def _add(self, obj: Dict[str, Optional[Dict]], parts: Union[List[str], Tuple[str]]) -> None:
        """
        Adds the path parts to the object.

        Parameters:
        obj (dict): Object that will be edited.
        path (list): The listed parts of a path that will be added to the obj.
        """
        import datetime

        def update_properties(
            properties: Dict[str, bool],
            file: bool = False,
            stored: bool = False,
            stored_in: datetime.datetime = None
        ) -> None:
            """
            Changes the properties of the stored part.

            Parameters:
            properties (Dict[str, bool]):
            file (bool, optional): . Defaults to False.
            stored (bool, optional): . Defaults to False.
            stored_in (datetime.datetime, optional): . Defaults to None.
            """
            properties["file"] = file
            properties["stored"] = stored
            properties["stored_in"] = stored_in

        time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        for part in parts:
            is_file = self.to_path(parts).is_file()
            is_stored = part == parts[-1]

            if part not in obj:
                obj[part] = {}
                # Defines the property object.
                obj[part]["//"] = self.path_properties.copy()
                update_properties(
                    properties=obj[part]["//"],
                    file=is_file,
                    stored=is_stored,
                    stored_in=time if is_stored else None
                )
            else:
                if is_stored:
                    # Update the stored_in if this is the stored part.
                    update_properties(
                        properties=obj[part]["//"],
                        file=is_file,
                        stored=is_stored,
                        stored_in=time,
                    )

            obj = obj[part]

    def remove_path(self, path: str) -> None:
        """
        Removes the managed path.

        Parameters:
        path (str): Path that will be removed.
        """
        path_obj = self.to_path(path=path)
        self._rm(obj=self.data, parts=path_obj.parts)

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
        path_obj = self.to_path(path=path)
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
        Path that will be added.

        Parameters:
        path (str): 
        """
        path_obj = self.to_path(path=path)
        self._add(obj=self.data, parts=path_obj.parts)

    def load(self, fp: str) -> None:
        """
        Loads a new path to be managed.

        Parameters:
        fp (str): File that will be managed.
        """
        with open(str(fp), "r") as file:
            new_data = json.load(file)
            self.set_data(data=new_data)

    def to_path(self, path: Union[str, List[str], Tuple[str]]) -> pathlib.Path:
        """
        Returns the path instance of the 'pathlib.Path' class.

        Parameters:
        path (Union[str, List[str], Tuple[str]]): Path for transformation into `Path` object.

        Returns:
        pathlib.Path: Path instance.
        """
        path_class = pathlib.Path
        if isinstance(path, str):
            path_object = path_class(path.lower())
        elif isinstance(path, (list, tuple)):
            path_object = path_class(*list(part.lower() for part in path))
        else:
            raise TypeError(msg["type_error"].format(f"{str.__name__}, {list.__name__}", type(path).__name__))
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
            self.remove_path(path=path)

    def strorage_rm(self, path: str) -> None:
        """
        Removes the storage path without removing the nesting.

        Parameters:
            path (str): Path to be removed from storage.
        """
        path_obj = self.to_path(path=path)
        parts = path_obj.parts
        obj = self.data
        for part in parts:
            obj = obj[part]
            if part == parts[-1]:
                obj["//"] = self.path_properties.copy()

    def _rm(self, obj: Dict[str, Optional[dict]], parts: List[str]) -> None:
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

    def save(self, fp: str) -> None:
        """
        Saves data to the storage file if the file is not None.
        """
        with open(str(fp), "w") as file:
            json.dump(self.data, file, indent=2)

    def set_data(self, data: Dict[str, Optional[dict]]) -> None:
        """
        Resets the managed data.

        Parameters:
        data: Dict[str, Optional[dict]]: Data that will be managed.
        """
        if not isinstance(data, dict):
            raise TypeError(msg["type_error"].format(str.__name__, type(data).__name__))
        setattr(self, "data", data)
