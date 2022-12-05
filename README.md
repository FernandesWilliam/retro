# GitHub action analyser

## Development
```shell
python -m pip install -r requirements.txt
```

## Execution
```shell
docker-compose up
```

By default, the application follows the behaviour described in [config/run-config.yaml](./config/run-config.yaml). You 
can change the behaviour by updating this file or create a new one that follows the same structure and change the
[docker image entrypoint](./Dockerfile) argument by your filename.

```shell
python3 main.py config/run-config.yaml
```