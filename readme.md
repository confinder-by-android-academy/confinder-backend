### Start localy

 To start locally, install dependencies:
 
 ```bash
pipenv install
```

and run

```bash
aioworkeres -c confinder/config.yaml
```

### Doc

Swagger doc is available to on `/docs` endpoint

api.yaml is swagger doc, which can be used as API doc.

### Docker

You can run localy with docker-compose by:

```bash
docker-compose up --build
```

### Usage

To test application you can start it locally, go to `http://localhost:8080/`, and click `Validate`.

It will run `localhost:5000/testing_container` solution with fake dataset.

To push another container, you should build it, tag with `localhost:5000/testing_container` and push with docker.


### Setting app

Application is setting up by environment variables:

- MONGO_URI - uri of mongo db, example `mongodb://localhost:27017/`

### Requirements