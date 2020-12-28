import json
import os

import yaml
from fastapi import FastAPI
from pydantic.main import BaseModel
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from server import static
from server.model import ProjectConfig


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
        result=GenDockerfile().gen(yaml_content=yaml_content.yaml_file_content)
    )


class GenDockerfile:

    def __yaml_to_obj(self, yaml_content: str) -> ProjectConfig:
        yml = yaml.load(yaml_content)
        proj_cfg = ProjectConfig.parse_raw(json.dumps(yml))
        return proj_cfg

    def gen(self, yaml_content: str):
        proj_cfg = self.__yaml_to_obj(yaml_content)
        docker_file_lines = []
        docker_file_lines.append(f"FROM {proj_cfg.base_image}")
        docker_file_lines.append(f"MAINTAINER Razorthink (https://www.razorthink.com)")
        docker_file_lines.append(f'LABEL description="{proj_cfg.description}"')
        docker_file_lines.append(f'LABEL base_os="{proj_cfg.base_os}"')
        docker_file_lines.append(f'LABEL base_os_flavor="{proj_cfg.base_os_flavor}"')
        dockerfile = "\n".join(docker_file_lines)
        print(dockerfile)
        return dockerfile
