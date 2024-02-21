# Simple python flask file server

## Task assignment

- implement in python (use of any libraries and DB services is optional)
- upload, download, delete file
- list files available on file server (with filtering options)
- statistics of files available on file server
- uploaded file has following metadata:
  - name
  - extension type
  - size
  - upload datetime

### Prerequisites

- small files - max. 100 MiB, but most of the arround 1 MiB
- a lot of files
- used mainly via JS from web browser
- authentication and authorization is not needed
- more reading than writing

## Dependencies

- solution is dockerized, so you need docker installed on your system
- `curl` for manual tests

## How to run

Extract provided ZIP file.

```bash
cd PROJECT_FOLDER
docker build -t file-server .
docker run -p 5000:5000 file-server
```

Now you can play with file server in another terminal window, web browser, or elsewhere :).

Files are not persistent. Restarted docker service will start empty.

## Endpoints

### Upload file - /upload - POST

- `curl -X POST -F "file=@PATH_TO_YOUR_FILE" http://localhost:5000/file`
- returns:

```json
{
    "file_info":
        {
            "datetime_uploaded": ISO DATETIME as STRING,
            "name": STRING,
            "size_bytes": INT,
            "type": STRING
        },
    "message": STRING
}
```

Upload of new file with same name will overwrite the old one. Max upload size of one file is 100 MiB.

### Download file - /file - GET

- `curl -o OUTPUT_FILE_NAME http://localhost:5000/file/TARGET_FILE_NAME`

### Delete file - /file - DELETE

- `curl -X DELETE http://localhost:5000/file/TARGET_FILE_NAME`
- returns:

```json
{
    "message": STRING
}
```

### List files - /file - GET

- `curl http://localhost:5000/file`
  - with type filtering `curl http://localhost:5000/file?type=.md`
  - with name ordering ascending `curl http://localhost:5000/file?sort_by_size=asc`
  - with name ordering descending `curl http://localhost:5000/file?sort_by_size=desc`
  - or you can combine it like this `curl "http://localhost:5000/file?type=.md&sort_by_size=asc"`
- returns:

```json
{
    "files":
        [
            {
                "datetime_uploaded": ISO DATETIME as STRING,
                "name": STRING,
                "size_bytes": INT,
                "type": STRING
            }
        ]
}
```

### Statistics - /file/statistics - GET

- `curl http://localhost:5000/file/statistics`
- return:

```json
{
    "avg_size_bytes": INT,
    "median_size_bytes": INT,
    "num_of_files": INT,
    "total_size_bytes": INT
}
```

## Notes to discuss

- how to handle file persistence
- README documents only happy path responses
- possible authorization / authentification
- how to not overwrite files with same name
- I deliberately avoided all comments - code is short and straightforward
  - when possible - put all info into code, not into comments
  - in production code I like to use google style docstrings - [github example](https://gist.github.com/redlotus/3bc387c2591e3e908c9b63b97b11d24e)
- I do not follow PEP 8 line length
  - usually I like to use limit around ~ 120 characters per line - but it is all about consensus in team
  - integration of static type checking, linters and code formatter, I like to use following:
  - mypy - [github link](https://github.com/python/mypy)
  - ruff - [github link](https://github.com/astral-sh/ruff)