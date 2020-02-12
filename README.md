# fastapi-basic-mongodb-example
Basic Structure for FastAPI that uses Motor (Async MongoDB Driver)

## Run MongoDB Locally
open terminal and run
```bash
mongod
```

### Installation

```bash
cd src
pip install -r ./requirements.txt
```

## Run FastAPI server

```bash
uvicorn app.main:app --reload
```


## Access Swagger Documentation
```bash
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```
