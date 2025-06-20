import copy
import random
from typing import Any, Callable, Optional, Union, cast, List

import jsonc
from pydantic import BaseModel
from ..s3 import S3Client, S3Config
from .distribution import Distribution, DistributionConfig, sample_field_value
from ..memory.const import SocialRelation

__all__ = [
    "MemoryConfigGenerator",
    "MemoryT",
    "StatusAttribute",
    "default_memory_config_citizen",
]


class StatusAttribute(BaseModel):
    name: str  # the name of the attribute
    type: type  # the type of the attribute
    default: Any  # the default value of the attribute
    description: str  # the description of the attribute
    whether_embedding: bool = False  # whether the attribute is vectorized
    embedding_template: Optional[str] = None  # the template to generate the value


MemoryT = Union[tuple[type, Any], tuple[type, Any, bool], tuple[type, Any, bool, str]]
"""
MemoryT is a tuple of (type, value, use embedding model, embedding template)
- type: the type of the value
- value: the value
- use embedding model (optional): whether the value is generated by embedding model
- embedding template (optional): the template to generate the value
"""


def default_memory_config_citizen(
    distributions: dict[str, Distribution],
    class_config: Optional[list[StatusAttribute]] = None,
) -> tuple[dict[str, MemoryT], dict[str, MemoryT], dict[str, Any]]:
    EXTRA_ATTRIBUTES = {}

    # extra attributes from class config
    if class_config:
        for attr in class_config:
            if attr.name in EXTRA_ATTRIBUTES:
                continue
            if attr.embedding_template:
                EXTRA_ATTRIBUTES[attr.name] = (
                    attr.type,
                    attr.default,
                    attr.whether_embedding,
                    attr.embedding_template,
                )
            else:
                EXTRA_ATTRIBUTES[attr.name] = (
                    attr.type,
                    attr.default,
                    attr.whether_embedding,
                )

    PROFILE = {
        "name": (str, "unknown", True),
        "gender": (str, "unknown", True),
        "age": (int, 20, True),
        "education": (str, "unknown", True),
        "skill": (str, "unknown", True),
        "occupation": (str, "unknown", True),
        "family_consumption": (str, "unknown", True),
        "consumption": (str, "unknown", True),
        "personality": (str, "unknown", True),
        "income": (float, 5000, True),
        "currency": (float, 30000, True),
        "residence": (str, "unknown", True),
        "city": (str, "unknown", True),
        "race": (str, "unknown", True),
        "religion": (str, "unknown", True),
        "marriage_status": (str, "unknown", True),
        "background_story": (str, "No background story", True),
        "social_network": (list[SocialRelation], [], False),
    }

    BASE = {
        "home": {
            "aoi_position": {"aoi_id": sample_field_value(distributions, "home_aoi_id")}
        },
        "work": {
            "aoi_position": {"aoi_id": sample_field_value(distributions, "work_aoi_id")}
        },
    }

    return EXTRA_ATTRIBUTES, PROFILE, BASE


def default_memory_config_supervisor(
    distributions: dict[str, Distribution],
    class_config: Optional[list[StatusAttribute]] = None,
) -> tuple[dict[str, MemoryT], dict[str, MemoryT], dict[str, Any]]:
    EXTRA_ATTRIBUTES = {}

    # extra attributes from class config
    if class_config:
        for attr in class_config:
            if attr.name in EXTRA_ATTRIBUTES:
                continue
            if attr.embedding_template:
                EXTRA_ATTRIBUTES[attr.name] = (
                    attr.type,
                    attr.default,
                    attr.whether_embedding,
                    attr.embedding_template,
                )
            else:
                EXTRA_ATTRIBUTES[attr.name] = (
                    attr.type,
                    attr.default,
                    attr.whether_embedding,
                )

    PROFILE = {
        "name": (str, "unknown", True),
        "gender": (str, "unknown", True),
        "age": (int, 20, True),
        "education": (str, "unknown", True),
        "skill": (str, "unknown", True),
        "occupation": (str, "unknown", True),
        "family_consumption": (str, "unknown", True),
        "consumption": (str, "unknown", True),
        "personality": (str, "unknown", True),
        "income": (float, 5000, True),
        "currency": (float, 30000, True),
        "residence": (str, "unknown", True),
        "city": (str, "unknown", True),
        "race": (str, "unknown", True),
        "religion": (str, "unknown", True),
        "marriage_status": (str, "unknown", True),
        "background_story": (str, "No background story", True),
        "social_network": (list[SocialRelation], [], False),
    }

    BASE = {}

    return EXTRA_ATTRIBUTES, PROFILE, BASE


class MemoryConfigGenerator:
    """
    Generate memory configuration.
    """

    def __init__(
        self,
        config_func: Callable[
            [dict[str, Distribution], Optional[list[StatusAttribute]]],
            tuple[dict[str, MemoryT], dict[str, MemoryT], dict[str, Any]],
        ],
        class_config: Optional[list[StatusAttribute]] = None,
        number: Optional[int] = None,
        file: Optional[str] = None,
        distributions: dict[str, Union[Distribution, DistributionConfig]] = {},
        s3config: S3Config = S3Config.model_validate({}),
    ):
        """
        Initialize the memory config generator.

        - **Args**:
            - `config_func` (Callable): The function to generate the memory configuration.
            - `file` (Optional[str]): The path to the file containing the memory configuration.
            - `distributions` (dict[str, Distribution]): The distributions to use for the memory configuration. Default is empty dict.
            - `s3config` (S3Config): The S3 configuration.
        """
        self._memory_config_func = config_func
        self._class_config = class_config
        self._number = number
        self._file_path = file
        self._s3config = s3config
        if file is not None:
            self._memory_data = _memory_config_load_file(file, s3config)
            if self._number is not None:
                if self._number > len(self._memory_data):
                    raise ValueError(
                        f"Number of agents is greater than the number of entries in the file ({self._file_path}). Expected {self._number}, got {len(self._memory_data)}"
                    )
                self._memory_data = self._memory_data[: self._number]
        else:
            self._memory_data = None
        distributions = copy.deepcopy(distributions)
        # change DistributionConfig to Distribution
        for field, distribution in distributions.items():
            if isinstance(distribution, DistributionConfig):
                distributions[field] = Distribution.from_config(distribution)
        self._distributions = cast(dict[str, Distribution], distributions)

    def merge_distributions(
        self, distributions: dict[str, Union[Distribution, DistributionConfig]]
    ):
        """
        Merge the distributions for the memory config generator.
        """
        distributions = copy.deepcopy(distributions)
        # change DistributionConfig to Distribution
        for field, distribution in distributions.items():
            if field in self._distributions:
                raise ValueError(f"Distribution {field} is already set")
            else:
                if isinstance(distribution, DistributionConfig):
                    distributions[field] = Distribution.from_config(distribution)
                self._distributions[field] = distributions[field]  # type: ignore

    def generate(self, i: int):
        """
        Generate memory configuration.

        Args:
            i (int): The index of the memory configuration to generate. Used to find the i-th memory configuration in the file.

        Returns:
            tuple[dict[str, MemoryT], dict[str, MemoryT], dict[str, Any]]: The memory configuration.
        """
        extra_attrs, profile, base = self._memory_config_func(
            self._distributions, self._class_config
        )
        if self._memory_data is not None:
            if i >= len(self._memory_data):
                raise ValueError(
                    f"Index out of range. Expected index <= {len(self._memory_data)}, got: {i}"
                )
            memory_data = self._memory_data[i]
        else:
            memory_data = {}
        return _memory_config_merge(memory_data, extra_attrs, profile, base)

    def get_agent_data_from_file(self) -> List[dict]:
        """
        Get agent data from file.

        - **Description**:
            - Retrieves the raw agent data from the file specified during initialization.
            - This is used when agents need to be created with IDs from the file.

        - **Returns**:
            - `List[dict]`: A list of agent data dictionaries from the file.

        - **Raises**:
            - `ValueError`: If no file was specified during initialization.
        """
        if self._file_path is None:
            raise ValueError("No file was specified during initialization")

        if self._memory_data is None:
            self._memory_data = _memory_config_load_file(
                self._file_path, self._s3config
            )

        return self._memory_data


def _memory_config_load_file(file_path: str, s3config: S3Config):
    """
    Loads the memory configuration from the given file.
    - **Description**:
        - Loads the memory configuration from the given file.
        - Supports both .json and .jsonl file types.
        - For .json files, returns the parsed JSON content.
        - For .jsonl files, returns a list of parsed JSON objects from each line.

    - **Args**:
        - `file_path` (str): The path to the file containing the memory configuration.

    - **Returns**:
        - `memory_data` (Union[dict, list]): The memory data - either a single object or list of objects.

    - **Raises**:
        - `ValueError`: If the file type is not supported.
    """
    # Check file extension
    if s3config.enabled:
        s3client = S3Client(s3config)
        data_bytes = s3client.download(file_path)
        data_str = data_bytes.decode("utf-8")
    else:
        with open(file_path, "r") as f:
            data_str = f.read()

    if file_path.endswith(".json"):
        memory_data = jsonc.loads(data_str)
        if not isinstance(memory_data, list):
            raise ValueError(
                f"Invalid memory data. Expected a list, got: {memory_data}"
            )
        return memory_data
    elif file_path.endswith(".jsonl"):
        memory_data = []
        for line in data_str.splitlines():
            if line.strip():  # Skip empty lines
                memory_data.append(jsonc.loads(line))
        return memory_data
    # TODO：add support for csv file
    else:
        raise ValueError(
            f"Unsupported file type. Only .json or .jsonl files are supported. Got: {file_path}"
        )


def _memory_config_merge(
    file_data: dict,
    base_extra_attrs: dict[str, MemoryT],
    base_profile: dict[str, MemoryT],
    base_base: dict[str, Any],
) -> dict[str, Any]:
    """
    Merges memory configuration from file with base configuration.

    - **Description**:
        - Takes file data and merges it with base configuration components.
        - Special handling for 'home' and 'work' fields which may need to be placed in correct section.

    - **Args**:
        - `file_data` (dict): Memory configuration data loaded from file.
        - `base_extra_attrs` (dict): Base extra attributes configuration.
        - `base_profile` (dict): Base profile configuration.
        - `base_base` (dict): Base memory configuration.

    - **Returns**:
        - `dict`: Merged memory configuration with proper structure.
    """
    # Create copies to avoid modifying the originals
    extra_attrs = base_extra_attrs.copy()
    profile = base_profile.copy()
    base = base_base.copy()

    # Special handling for home and work locations
    location_fields = ["home", "work"]

    for key, value in file_data.items():
        # Check where this key exists in the base configuration
        if key in extra_attrs:
            extra_attrs[key] = extra_attrs[key][:1] + (value, ) + (extra_attrs[key][2:] if len(extra_attrs[key]) > 2 else ())
        elif key in profile:
            profile[key] = profile[key][:1] + (value, ) + (profile[key][2:] if len(profile[key]) > 2 else ())
        elif key in location_fields:
            # Typically these would go in profile, but follow your specific needs
            base[key] = {"aoi_position": {"aoi_id": value}}
        else:
            # For any new fields not in base config, add to extra_attrs
            extra_attrs[key] = value

    return {"extra_attributes": extra_attrs, "profile": profile, "base": base}
