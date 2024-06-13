# Messenger

Base usage:
```
> poetry shell
(osiris-py3.10) > source run.sh 
<...>
INFO:     Uvicorn running on http://127.0.0.1:8081 (Press CTRL+C to quit)

```

# sqlite:
```
data.db
SQLite version 3.37.2 2022-01-06 13:25:41
Enter ".help" for usage hints.
sqlite> .tables
Chat             Message          User             alembic_version
sqlite> 

// or
(osiris-py3.10) > sqlite3 
sqlite> attach database 'data.db' as osiris;
sqlite> .tables
```

# ToDo
- !!One!! standart of docstrings
- testing
- docker

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

# alembic # TODO!
For managing migrations we use alembic ((article url)[https://habr.com/ru/companies/yandex/articles/511892/]):
```
(osiris-py3.10) > alembic init alembic # initialisation of alembic
(osiris-py3.10) > alembic init -t async migrations # initialisation of alembic for working with async sqlalchemy

(osiris-py3.10) > alembic revision --message="Initial" --autogenerate
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected removed index 'ix_Message_id' on 'Message'
INFO  [alembic.autogenerate.compare] Detected removed table 'Message'
INFO  [alembic.autogenerate.compare] Detected removed index 'ix_User_id' on 'User'
INFO  [alembic.autogenerate.compare] Detected removed table 'User'
INFO  [alembic.autogenerate.compare] Detected removed index 'ix_Chat_id' on 'Chat'
INFO  [alembic.autogenerate.compare] Detected removed table 'Chat'
  Generating /home/valehin/projects/test_projects/webmessenger/alembic/versions/f81ed92dbb64_initial.py ...  done

# При этом надо импорты моделей поддерживать в актуальному состоянии!
(osiris-py3.10) valehin@valehin-ThinkBook-15-G2-ITL:~/projects/test_projects/webmessenger$ alembic revision --message="Added users_chats" --autogenerate
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'Users_Chats'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_Users_Chats_id'' on '('id',)'
  Generating /home/valehin/projects/test_projects/webmessenger/alembic/versions/2b189f1e8392_added_users_chats.py ...  done
(osiris-py3.10) valehin@valehin-ThinkBook-15-G2-ITL:~/projects/test_projects/webmessenger$ git push origin HEAD^C
(osiris-py3.10) valehin@valehin-ThinkBook-15-G2-ITL:~/projects/test_projects/webmessenger$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade e66ad7d1cc42 -> 2b189f1e8392, Added users_chats
(osiris-py3.10) valehin@valehin-ThinkBook-15-G2-ITL:~/projects/test_projects/webmessenger$ 

```
