# dns-updator
Small Python script for easily updating a DNS zone in CLI using the OVH API.
⚠️ This script is not production ready ! Please use this with care

# Dependencies

```
pip install ovh
pip install python-dotenv
```

## OVH API Scopes

```
GET /me
GET /domains/*
PUT /domains/*
POST /domains/*
DELETE /domains/*
```

You can adjust the scopes with your preferences.

## Usage

Create the `.env` file  : 

```
cp .env.example .env
```

Fill the file with your OVH credentials and launch the script ! 