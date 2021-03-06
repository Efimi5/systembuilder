import os
import json
import yaml
import shutil

from src.main.builder import Builder
from src.main.manifest import Manifest
from time import sleep


def test_clone_repo():
    builder = Builder(Manifest())
    builder.clone_repo('https://github.com/antonkurenkov/systembuilder.git')
    # waiting while cloning
    sleep(5)
    assert os.path.isfile('./repo/README.md')
    # deleting directory after testing, might not work on windows because can't delete .git file.
    # shutil.rmtree('./repo', ignore_errors=True)


def test_generate_status_file_with_error():
    builder = Builder(Manifest())
    builder.generate_status_file(False, 'error')
    assert os.path.isfile('status.json')
    with open('status.json') as status_file:
        status = json.load(status_file)
    assert not status['status']
    assert status['message'] == 'error'
    os.remove('status.json')


def test_generate_status_file_without_error():
    builder = Builder(Manifest())
    builder.generate_status_file(True)
    assert os.path.isfile('status.json')
    with open('status.json') as status_file:
        status = json.load(status_file)
    assert status['status']
    assert status['message'] == ""
    os.remove('status.json')


def test_create_dockerfile():
    builder = Builder(Manifest())
    data = {'docker': {'dockerfile': 'FROM python:latest\nENTRYPOINT ["python"]', 'parameters': ['some parameter']}}
    with open('info.yaml', 'w') as file:
        yaml.dump(data, file)
    builder.create_dockerfile('info.yaml')
    assert os.path.isfile('DOCKERFILE')
    with open('DOCKERFILE', 'r') as dockerfile:
        fst_line = dockerfile.readline()
    assert fst_line == 'FROM python:latest\n'
    os.remove('info.yaml')
    os.remove('DOCKERFILE')
