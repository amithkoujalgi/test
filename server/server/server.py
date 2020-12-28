import json
import os

import yaml
from fastapi import FastAPI
from pydantic.main import BaseModel
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from server import static
from server.model import ProjectConfig, PipPackage, PublishedPackageSystemPackage, PublishedPackage, \
    EnvironmentVariable


class ReqBody(BaseModel):
    yaml_file_content: str


static_files_path = os.path.dirname(static.__file__)
app = None

app = FastAPI(debug=True, title="API Spec",
              description="REST API playground",
              version="0.0.1")
app.mount("/static", StaticFiles(directory=static_files_path, html=True), name="static")


@app.get("/")
async def read_index():
    return RedirectResponse(url="/static")


origins = ["*"]


@app.post("/generate-dockerfile")
async def generate(yaml_content: ReqBody):
    return dict(
        result=GenDockerfile(yaml_content=yaml_content.yaml_file_content).gen()
    )


class GenDockerfile:
    proj_cfg = None

    def __init__(self, yaml_content: str):
        self.proj_cfg = self.__yaml_to_obj(yaml_content)

    def __yaml_to_obj(self, yaml_content: str) -> ProjectConfig:
        yml = yaml.load(yaml_content)
        return ProjectConfig.parse_raw(json.dumps(yml))

    def gen(self):
        docker_file_lines = []
        docker_file_lines.append(f"FROM {self.proj_cfg.base_image}\n")
        docker_file_lines.append(f'LABEL maintainer="Tenant User - XYZ <xyc@somedomain.com>"')
        docker_file_lines.append(f'LABEL project="{self.proj_cfg.name}"')
        docker_file_lines.append(f'LABEL description="{self.proj_cfg.description}"')
        docker_file_lines.append(f'LABEL base_os="{self.proj_cfg.base_os}"')
        docker_file_lines.append(f'LABEL base_os_flavor="{self.proj_cfg.base_os_flavor}"')

        base_img_pip_pkgs = [f"{i.name}=={i.version}" for i in self.proj_cfg.base_image_config.pip_packages]
        base_img_pip_pkgs = ", ".join(base_img_pip_pkgs)
        docker_file_lines.append(f'LABEL base_image_pip_libs="{base_img_pip_pkgs}"')

        base_img_sys_pkgs = [f"{i.name}" for i in self.proj_cfg.base_image_config.system_packages]
        base_img_sys_pkgs = ", ".join(base_img_sys_pkgs)
        docker_file_lines.append(f'LABEL base_image_sys_libs="{base_img_sys_pkgs}"')

        base_img_envs = [f"{i.variable}='{i.value}'" for i in self.proj_cfg.base_image_config.environment_variables]
        base_img_envs = ", ".join(base_img_envs)
        docker_file_lines.append(f'LABEL base_image_env_vars="{base_img_envs}"')

        docker_file_lines.append(f'\n# Env Vars - user added\n')
        env_var: EnvironmentVariable
        for env_var in self.proj_cfg.environment_variables:
            docker_file_lines.append(f'ENV {env_var.variable}="{env_var.value}"')

        docker_file_lines.append(f'\n# System packages - user added\n')
        sys_pkg: PublishedPackageSystemPackage
        for sys_pkg in self.proj_cfg.project_libraries.system_packages:
            docker_file_lines.append(f'RUN apt-get install -y {sys_pkg.name}')

        docker_file_lines.append(f"\n# Project's Pip packages - user added\n")
        pip_lib: PipPackage
        for pip_lib in self.proj_cfg.project_libraries.pip_packages:
            docker_file_lines.append(f'RUN pip install {pip_lib.name}=={pip_lib.version}')

        docker_file_lines.append(f"\n# Published packages - user added")
        docker_file_lines.append(f"\n# Reference for Pip package installation from external URLs - https://stackoverflow.com/a/57552988/1335709\n")

        published_lib: PublishedPackage
        for published_lib in self.proj_cfg.project_libraries.published_packages:
            docker_file_lines.append(
                f'# START: Config for user added published package: {published_lib.name}')

            repo = ""
            if 'market' in published_lib.source.lower():
                repo = "https://gcp-marketplace-repo.razorthink.com"
            elif 'tenant' in published_lib.source.lower():
                repo = "https://gcp-tenant-repo.razorthink.com"
            else:
                repo = "invalid-source"

            published_sys_lib: PublishedPackageSystemPackage
            for published_sys_lib in published_lib.system_packages:
                docker_file_lines.append(
                    f'RUN apt-get install -y {published_sys_lib.name}')

            published_pip_lib: PublishedPackageSystemPackage
            for published_pip_lib in published_lib.pip_packages:
                docker_file_lines.append(f'RUN pip install {published_pip_lib.name}=={published_pip_lib.version}')

            published_env_var: EnvironmentVariable
            for published_env_var in published_lib.environment_variables:
                docker_file_lines.append(f'ENV {published_env_var.variable}="{published_env_var.value}"')

            docker_file_lines.append(
                f'RUN pip install {published_lib.name}=={published_lib.version} \n\t--extra-index-url={repo} \n\t--trusted-host={repo.replace("https", "")}')

            docker_file_lines.append(
                f'# END: Config for user added published package: {published_lib.name}\n')

        dockerfile = "\n".join(docker_file_lines)
        print(dockerfile)
        return dockerfile
