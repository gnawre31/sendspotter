# SendSpotter

Tracks rock climbing shoe sales 

## Architecture
![alt text](https://github.com/gnawre31/sendspotter/blob/main/sendspotter.jpg?raw=true)


## Setup

Cloning

```
  git clone https://github.com/gnawre31/climbing-shoe-alerts.git
  cd climbing-shoe-alerts
```

Python

```
  pip install virtualenv
  python3.11 -m venv env
  source env/bin/activate
  pip install -r requirements.txt
```

Client

```
  cd client
  npm install
```

ENV
rename sample.env to ".env" and fill in environment variables

```
  TYPE=
  PROJECT_ID=
  PRIVATE_KEY_ID=
  PRIVATE_KEY=
  CLIENT_EMAIL=
  CLIENT_ID=
  AUTH_URI=
  TOKEN_URI=
  AUTH_PROVIDER_X509_CERT_URL=
  CLIENT_X509_CERT_URL=
  UNIVERSE_DOMAIN=
  
  SHEET_ID=
  ALL_RANGE=
  ID_RANGE=
```
## AWS ECR
Push dockerized AWS Lambda code to ECR
```
  cd [dir]
  sls deploy
```

## Client scripts

Running dev server
```
  cd client
  npm run dev
```

Deploying 
```
  cd client
  npm run predeploy
  npm run deploy
```
