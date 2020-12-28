from typing import List, Optional

from pydantic.main import BaseModel


class EnvironmentVariable(BaseModel):
    variable: Optional[str] = None
    type: Optional[str] = None
    value: Optional[str] = None
    desc: Optional[str] = None


class BaseImageLibrariesPipPackage(BaseModel):
    name: Optional[str] = None
    version: Optional[float] = None


class BaseImageConfig(BaseModel):
    pip_packages: Optional[List[BaseImageLibrariesPipPackage]] = None
    system_packages: Optional[List[BaseImageLibrariesPipPackage]] = None
    environment_variables: Optional[List[EnvironmentVariable]] = None


class PipPackage(BaseModel):
    name: Optional[str] = None
    version: Optional[float] = None
    user_uploaded: Optional[bool] = None
    added_by: Optional[str] = None
    added_on: Optional[str] = None
    updated_by: Optional[str] = None
    updated_on: Optional[str] = None


class PublishedPackageSystemPackage(BaseModel):
    name: Optional[str] = None
    version: Optional[float] = None
    added_by: Optional[str] = None
    added_on: Optional[str] = None
    updated_by: Optional[str] = None
    updated_on: Optional[str] = None


class PublishedPackage(BaseModel):
    name: Optional[str] = None
    version: Optional[float] = None
    source: Optional[str] = None
    added_by: Optional[str] = None
    added_on: Optional[str] = None
    updated_by: Optional[str] = None
    updated_on: Optional[str] = None
    pip_packages: Optional[List[PublishedPackageSystemPackage]] = None
    system_packages: Optional[List[PublishedPackageSystemPackage]] = None
    environment_variables: Optional[List[EnvironmentVariable]] = None


class ProjectLibraries(BaseModel):
    published_packages: Optional[List[PublishedPackage]] = None
    pip_packages: Optional[List[PipPackage]] = None
    system_packages: Optional[List[PublishedPackageSystemPackage]] = None


class ProjectConfig(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    added_by: Optional[str] = None
    added_on: Optional[str] = None
    updated_by: Optional[str] = None
    updated_on: Optional[str] = None
    base_image: Optional[str] = None
    base_os: Optional[str] = None
    base_os_flavor: Optional[str] = None
    base_image_config: Optional[BaseImageConfig] = None
    project_libraries: Optional[ProjectLibraries] = None
    environment_variables: Optional[List[EnvironmentVariable]] = None
    additional_commands: Optional[List[str]] = None
    default_entrypoint: Optional[str] = None
