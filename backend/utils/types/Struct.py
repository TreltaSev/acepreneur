from utils.helper import find, requires
from typing import Any, List
import json

_undefined = object()


class Struct:
    """
    Converts a nested dictionary object into a discoverable object
    Example:
    ```python
    j: dict = {"a": "b", "c": {"d": "e"}}
    j_struct = Struct(**j)
    print(j_struct.c.d) # "e"
    ```
    """

    def __init__(self, obj=None, **kwargs) -> None:

        if obj:
            if isinstance(obj, Struct):
                obj = obj.dict

            self.__dict__.update(obj)
        else:
            self.__dict__.update(**kwargs)

    @property
    def dict(self):
        return self.__dict__

    @property
    def unwrap(self):
        """
        Converts the top level structure with
        """
        result = {}
        for key, value in self.dict.items():
            if isinstance(value, Struct):
                result[key] = value.unwrap
            elif isinstance(value, list):
                result[key] = [
                    item.unwrap if isinstance(item, Struct) else item for item in value
                ]
            else:
                result[key] = value
        return result

    def has(self, key: str, fail: bool = False) -> bool:
        """
        Checks if the current structure contains a certain key

        :param str key: The Key mapping of the object in question
        :param bool fail: If this is true, raise `KeyError` on fail
        :returns bool: If the object has the key

        :raises KeyError: If `fail` is true and the key isn't found


        ## Example
        ```python
        structure: Struct = Struct({"key_in_question": None})

        structure.has("key_in_question") # True
        structure.has("key-in-question") # False
        structure.has("key-in-question", fail=True) # KeyError
        ```
        """

        does_have = hasattr(self, key)

        if not does_have and fail:
            raise KeyError(f"Structure Does not contain the key {key}")

        return does_have

    def get(self, key: str, default: Any = _undefined) -> Any:
        """
        Attempts to get a key from the current structure.

        :param str key: Key Mapping of the value
        :param Any default: Default fallback value

        :raises KeyError: if the key isn't found and a default isn't specified
        """

        if not self.has(key) and default is _undefined:
            raise KeyError(f"Key \"{key}\" not found in structure")

        return self.dict.get(key, default)

    def find_element(self, key: str, id: str, convert: Any) -> Any:
        """
        Used to find elements within allowed arrays.

        Parameters
        ----------

        `key : str`
            Array name, must be within the Savings.__allowed_keys list.            
        `id : str`
            id property matcher
        `convert : Any`
            Class that the account will be converted to.            
        """

        # Type Checking
        if key not in getattr(self, "_allowed_keys", []):
            raise TypeError(f"Un-allowed Search Key: {key}")

        account = find(getattr(self, key), property="id",
                       match=id, convert=convert, default=None)

        if not account:
            raise KeyError(f"Failed to find {key} with id: \"{id}\"")
        return account

    def requires(self, keys: List[str] | str):
        """
        Wrapper for the :meth utils.helper.requires: method

        :param keys: List of keys that this object requires
        :type keys: List[str]
        """
        
        if isinstance(keys, str):
            keys = [keys]
        
        return requires(self, keys)

    def filtered(self, keys: List[str]) -> dict:
        """
        Filters the object to include only the specified keys.

        Parameters
        ----------
        keys : List[str]
            List of keys to include in the resulting dictionary.

        Returns
        -------
        dict
            Dictionary containing only the specified keys that exist in the object.
        """
        return {key: self.dict[key] for key in keys if key in self.dict}

    def sanitized(self) -> dict:
        """
        Filters the object to include only keys with JSON serializable values.

        Returns
        -------
        dict
            Dictionary containing only keys with JSON serializable values.
        """
        result = {}
        for key, value in self.dict.items():
            try:
                json.dumps(value)  # Check if value is JSON serializable
                result[key] = value
            except (TypeError, OverflowError):
                continue
        return result

    def update(self, update_dict: dict = {}):
        """
        Updates the current structure with new values while respecting restricted keys.

        :param dict update_dict: Dictionary containing updated values
        """
        restrict: List[str] = []

        if hasattr(self, "restrict"):
            restrict = self.restrict

        def is_restricted(key_path):
            """Checks if a given key path is restricted."""
            for item in restrict:
                if key_path == item or key_path.startswith(item + "."):
                    return True
            return False

        def recursive_update(original, new_data, parent_key=""):
            """Recursively updates nested dictionaries."""
            for key, value in new_data.items():
                key_path = f"{parent_key}.{key}" if parent_key else key
                if is_restricted(key_path):
                    continue
                if isinstance(value, dict) and isinstance(original.get(key), dict):
                    recursive_update(original[key], value, key_path)
                else:
                    original[key] = value

        recursive_update(self.dict, update_dict)
