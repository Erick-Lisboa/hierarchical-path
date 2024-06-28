import json
import os
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

msg = {
    "TypeError": "The provided object must be a :class:`{}`, the provided object was: :class:`{}`",
    "FileNotFoundError": "Path \"{}\" was not found."
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
    properties: str
        Path properties symbol.
    """

    def __init__(
            self,
            storage_file: Optional[str] = None,
            data: Optional[Dict[str, Optional[Dict]]] = None,
        ) -> None:
        if storage_file is not None:
            self.load(fp=storage_file)
        else:
            self.data = {} if data is None else self.set_data(data=data)
        self.path_properties = {"file": False, "stored": False, "stored_in": None}
        self.properties = "//"

    def _add(self, obj: Dict[str, Dict], parts: Union[List[str], Tuple[str]]) -> None:
        """
        Adds the path parts to the object.

        Parameters:
        obj (Dict[str, Dict]): Object that will be edited.
        path (Union[List[str], Tuple[str]]): The listed parts of a path that will be added to the obj.

        Raises:
        FileNotFoundError: If the path is not found.
        """
        if not os.path.exists(os.path.join("/".join(parts))):
            raise FileNotFoundError(msg["FileNotFoundError"].format("/".join(parts)))

        import datetime

        def update_properties(
            properties: Dict[str, bool],
            file: bool = False,
            stored_: bool = False,
            stored_in: datetime.datetime = None,
        ) -> None:
            """
            Changes the properties of the stored part.

            Parameters:
            properties (Dict[str, bool]):
            file (bool): If the part is a file. Defaults to False.
            stored_ (bool): If the part is stored. Defaults to False.
            stored_in (datetime.datetime): Date the path was stored. Defaults to None.
            """
            properties["file"] = file if file is not None else properties["file"]
            properties["stored"] = stored_ if stored_ is not None else properties["stored"]
            properties["stored_in"] = stored_in if stored_in is not None else properties["stored_in"]

        time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        for part in parts:
            is_file = os.path.isfile(os.path.join("/".join(parts)))
            is_stored = part == parts[-1]

            if part not in obj:
                obj[part] = {}
                # Defines the property object.
                obj[part][self.properties] = self.path_properties.copy()
                update_properties(
                    properties=obj[part][self.properties],
                    file=is_file,
                    stored_=is_stored,
                    stored_in=time if is_stored else None,
                )
            else:
                if is_stored:
                    # Updates the stored_in if this is the stored part.
                    update_properties(
                        properties=obj[part][self.properties],
                        stored_=is_stored,
                        stored_in=time,
                    )

            obj = obj[part]

    def _get_all(self, obj: Dict[str, Dict], current_path: str = "") -> List[str]:
        """
        Gets the object's stored paths.

        Parameters:
            obj (Dict[str, Dict]): Object with stored paths.
            current_path (str): Current path.. Defaults to "".

        Returns:
            List[str]: List of stored paths.
        """
        paths = []
        obj_ = obj.copy()

        for part, apex in obj_.items():
            if part == self.properties:
                if apex["stored"]:
                    paths.append(current_path)
                continue
            new_path = f"{current_path}/{part}" if current_path else part.removesuffix("\\")
            paths.extend(self._get_all(apex, new_path))
        return paths

    def add_path(self, path: str) -> None:
        """
        Adds a new path.

        Parameters:
        path (str): Path that will be added.
        """
        if not path:
            return
        self._add(obj=self.data, parts=path.split("/"))

    def adds(self, paths: List[str]) -> None:
        """Adds the paths.

        Parameters:
            paths (List[str]): List of paths to be added.
        """
        for path in paths:
            self.add_path(path=path)

    def get_all(self) -> Union[List[str], List]:
        """
        Returns all stored paths.

        Returns:
        Union[List[str], List]: Stored paths.
        """
        return self._get_all(self.data)

    def get_data(self) -> Dict[str, Dict]:
        """
        Gets the current data.

        Returns:
        Dict[str, Dict]: Object being managed.
        """
        return getattr(self, "data")

    def get_properties(self, path: str) -> Dict[str, Dict]:
        """
        Returns the property object of a path.

        Parameters:
        path (str): Path in which its properties will be returned.

        Returns:
        Dict[str, Dict]: Path properties.
        """
        obj = self.data.copy()
        for part in path.split("/"):
            obj = obj[part]
        return obj[self.properties]

    def in_the_data(self, path: str) -> bool:
        """
        Returns whether the path is stored.

        Returns:
        bool: If the path is stored.
        """
        return path in self.get_all()

    def load(self, fp: str) -> None:
        """
        Loads a new path to be managed.

        Parameters:
        fp (str): File that will be managed.
        """
        with open(str(fp), "r") as file:
            new_data = json.load(file)
            self.set_data(data=new_data)

    def remove_path(self, path: str) -> None:
        """
        Removes the path.

        Parameters:
        path (str): Path that will be removed.
        
        Raises:
        FileNotFoundError: If the path is not found.
        """
        if not path:
            return
        elif not os.path.exists(os.path.join(path)):
            raise FileNotFoundError(msg["FileNotFoundError"].format(path))

        def __add(obj: Dict[str, Dict], parts: Union[List[str], Tuple[str]]) -> None:
            """
            Adds the path to the restructured data.

            Parameters:
            obj (Dict[str, Dict]): Object that will be edited.
            parts (Union[List[str], Tuple[str]]): The listed parts of a path that will be added to the obj.
            """
            for part in parts:
                properties = self.get_properties(path=path)
                if part not in obj:
                    obj[part] = {}
                    obj[part][self.properties] = properties if part == parts[-1] else self.path_properties
                obj = obj[part]

        paths = self.get_all()
        paths.remove(path)
        restructured_data = {}

        # Adds the paths without the removed path.
        for path in paths:
            parts = path.split("/")
            __add(obj=restructured_data, parts=parts)

        self.set_data(data=restructured_data)

    def removes(self, paths: List[str]) -> None:
        """
        Removes the paths.

        Parameters:
        paths (List[str]): List of paths that will be removed.
        """
        for path in paths:
            self.remove_path(path=path)

    def save(self, fp: str) -> None:
        """
        Saves data to the storage file.
        """
        with open(str(fp), "w") as file:
            json.dump(self.data, file, indent=2)

    def set_data(self, data: Dict[str, Dict]) -> None:
        """
        Sets the managed data.

        Parameters:
        data: Dict[str, Dict]: Data that will be managed.

        Raises:
        TypeError: If the data is not a dictionary.
        """
        if not isinstance(data, dict):
            raise TypeError(msg["type_error"].format(str.__name__, type(data).__name__))
        setattr(self, "data", data)
