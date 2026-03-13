# dns-updator
Small Python script for easily updating a DNS zone in CLI using the OVH API.

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