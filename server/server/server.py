import json
import os

import yaml
from fastapi import FastAPI
from pydantic.main import BaseModel
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from server import static
from server.model import ProjectConfig, PipPackage, PublishedPackageSystemPackage, PublishedPackage


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
        docker_file_lines.append(f'Label maintainer="Razorthink (https://www.razorthink.com)"')
        docker_file_lines.append(f'LABEL description="{self.proj_cfg.description}"')
        docker_file_lines.append(f'LABEL base_os="{self.proj_cfg.base_os}"')
        docker_file_lines.append(f'LABEL base_os_flavor="{self.proj_cfg.base_os_flavor}"')

        docker_file_lines.append(f'\n# System packages - user added\n')
        sys_pkg: PublishedPackageSystemPackage
        for sys_pkg in self.proj_cfg.project_libraries.system_packages:
            docker_file_lines.append(f'RUN apt-get install {sys_pkg.name}')

        docker_file_lines.append(f"\n# Project's Pip packages - user added\n")
        pip_lib: PipPackage
        for pip_lib in self.proj_cfg.project_libraries.pip_packages:
            docker_file_lines.append(f'RUN pip install {pip_lib.name}=={pip_lib.version}')

        docker_file_lines.append(f"\n# Published packages - user added")
        docker_file_lines.append(f"# Reference: https://stackoverflow.com/a/57552988/1335709\n")

        published_lib: PublishedPackage
        for published_lib in self.proj_cfg.project_libraries.published_packages:
            repo = ""
            if 'market' in published_lib.source.lower():
                repo = "https://gcp-marketplace-repo.razorthink.com"
            elif 'tenant' in published_lib.source.lower():
                repo = "https://gcp-tenant-repo.razorthink.com"
            else:
                repo = "invalid-source"
            docker_file_lines.append(
                f'RUN pip install {published_lib.name}=={published_lib.version} \n\t--extra-index-url={repo} \n\t--trusted-host={repo.replace("https", "")}')

        dockerfile = "\n".join(docker_file_lines)
        print(dockerfile)
        return dockerfile
