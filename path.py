import json
import pathlib
from typing import Dict, Optional, Union, List

class pathManager:
    """
    Path manager for hierarchical path storage.
    Manages a path to store it in a dictionary.

    Parameters:
    path (str): Path or  that will be managed.
    storage_file: Path of the .json file that will store and read the data for management

    Attributes:
    path (pathlib.Path): Managed path.
    data (dict): Hierarchical path storage data.
    storage_file (str): Path of the .json file that will store the data
    """
    def __init__(
            self,
            path: str,
            storage_file: Optional[str] = None,
        ) -> None:
        self.set_path(path)
        self.path: pathlib.Path 
        self.data = self.laod_data(storage_file) if storage_file else {}
        self.storage_file = storage_file

    def add(self, segment: Dict[str, Optional[Dict]], path: List[str]) -> None:
        """
        Repeat the path list by creating a new segment and adding.

        Parameters:
        segment (dict): New segment that will be edited.
        path (list): The listed path that will be added.
        """
        if not path:
            return

        current_element = path[0]
        if current_element not in segment:
            # Checks if the 'current element' is the last element of the path (file) if the path is not a directory.
            if self.path.is_file() and len(path) == 1:
                segment[current_element] = None
            else:
                segment[current_element] = {}

        # Passes the parameters so that the next element of the listed path is added to the data
        self.add(segment=segment[current_element], path=path[1:])

    def decrease(self) -> None:
        """
        Removes the managed path.
        """
    def find(self, path: str) -> Dict[str, Optional[Dict]]:
        """               
        Returns the segment of the past path.

        Parameters:
        path (str): The path that will be searched in the data.

        Returns:
        dict: The segment of the past path sought in the data.
        """
        segment = self.data
        path_obj = self.mk_path_obj(path=path)
        for part in path_obj.parts:
            segment = segment[part]
        return segment

    def get_all(self) -> Union[List[str], None]:
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
        return self.data

    def get_path(self, segment: Dict[str, Optional[Dict]]) -> str:
        """
        Returns the path of the past segment.

        Parameters:
        segment (dict): Segment that will take the path.

        Returns:
        str: Path collected in the data
        """
    def get_segment(self, path: str) -> Dict[str, Optional[Dict]]:
        """
        Returns the path segment in the data.

        Parameters:
        path: Path that will be collected in data.

        Returns:
        dict: Past path segment.
        """
    def get_stored(self) -> Union[Dict[str, Optional[Dict]], None]:
        """
        Returns the stored data if there is a file.

        Returns:
        dict: The stored data.
        None: If there is no data stored.
        """
    def in_the_data(self, path: str) -> bool:
        """
        Returns whether the path is in the data.

        Returns:
        bool: If the path is stored.
        """
    def increase(self) -> None:
        """
        Adds the managed path to the data.
        """
        self.add(segment=self.data, path=self.path.parts)

    def laod_data(self, storage_file: str) -> Optional[Dict[str, Optional[Dict]]]:
        """
        Load file from storage and set data attribute.
        """
        with open(str(storage_file), 'r') as file:
            return json.load(file)

    def mk_path_obj(self, path: str) -> pathlib.Path:
        """
        Returns the path instance of the 'pathlib.Path' class.

        Returns:
        pathlib.Path: Path instance.
        """
        if not isinstance(path, str):
            raise TypeError(f"'{path}' It is not string.")
        path_object = pathlib.Path(path)
        if not path_object.exists():
            raise NotADirectoryError(f"{path} Does not exist.")
        return path_object

    def remove(self, path: str) -> None:
        """
        Removes the past path.

        Parameters:
        path (str): Path that will be removed
        """
        if isinstance(path, str):
            path = self.mk_path_obj(path)
            
    def removes(self, paths: List[str]) -> None:
        """
        Removes the passed path if the path is in the data.

        Parameters:
        paths (List[str]): List of paths that will be removed.
        """
    def remove_file(self) -> None:
        """
        Removes the file from storage. Sets the 'data' attribute to None. 
        """
    def save(self) -> None:
        """
        Saves data to the storage file if the file is not None.
        """
        with open(self.storage_file, 'w') as file:
            json.dumps(file)

    def set_file(self, path: Optional[str]) -> None:
        """
        Defines the storage file, the 'data' attribute is changed to the file data and the data will be saved in the file.

        Parameters:
        path (str): The storage file.
        """
        self.storage_file = path

    def set_path(self, path: Optional[str]) -> None:
        """
        Defines the path that will be managed.

        Parameters:
        path (str): The path that will be the 'path' attribute.

        Raises:
        TypeError: If 'path' is not the 'str' instance.
        NotADirectoryError: If 'path' is not a directory.
        FileNotFoundError: If 'path' is not a file.
        """
        self.path = self.mk_path_obj(path=path)
