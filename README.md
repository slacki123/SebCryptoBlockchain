Install all packages:

```commandline
pip3 install -r requirements.txt
```

install node version 16
```commandline
choco install nodejs 16.13.2
```
or on linux

```shell
sudo apt-get install nodejs 16.13.2
```


if using the network as a peer, then get the tunnel connection to port localhost 5000 port of someone else running the node.
to get secure access to your wider access network, get the tunnel URL

Run
```commandline
npm install -g localtunnel
```

and then the following to return the URL
```commandline
lt --port 5000
```

Go to ./backend/app/__init__.py and ensure that you call the tunnelled URL and replace the existing chain upon connection.
This will allow the network to run properly

To run the api run
```commandline
python -m backend.app
```

Run frontend:

```commandline
cd c/../../SebCryptoBlockchain/frontend
npm run start
```
