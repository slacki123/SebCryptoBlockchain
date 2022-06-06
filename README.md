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
curl -s https://deb.nodesource.com/setup_16.x | sudo bash
sudo apt install nodejs -y
```


Install localtunnel so that python could use execute the command from within the code
Run
```commandline
npm install -g localtunnel
```

To run the api run
```commandline
python -m backend.app
```

Run frontend:

```commandline
cd c/../../SebCryptoBlockchain/frontend
npm run start
```
