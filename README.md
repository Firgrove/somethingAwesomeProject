# somethingAwesomeProject
End to end encrypted chat for security engineering course

### Getting Started - Backend

To run the backend we first need to install some dependencies

```console
python3 -m venv venv
source venv/bin/activate
```

```console
pip install -r requirements.txt
```

Now we can start the server

```console
python3 backend/server.py
```

### Getting Started - Frontend

First install dependencies

```console
npm install --global http-server
```

Once the http-server is installed, it can be started by running:

```console
npx http-server frontend -c 1 -p [port]
```