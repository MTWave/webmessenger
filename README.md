# Messenger

Base usage:
```
> poetry shell
(osiris-py3.10) > source run.sh 
<...>
INFO:     Uvicorn running on http://127.0.0.1:8081 (Press CTRL+C to quit)

```


# Poetry
This project uses poetry as package manager. 
https://python-poetry.org/docs/cli/

```
# activate poetry venv
> poetry shell

#  synchronize environment - and ensure it matches the lock file
(osiris-py3.10) > poetry install --sync 

# adds required packages to  pyproject.toml and installs them.
(osiris-py3.10) > poetry add requests

# deactivate
(osiris-py3.10) > exit  # deactivate
```