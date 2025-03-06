## Setting up project for development


Creating virtual environment <br />
`python3 -m venv venv`

Activating venv <br />
`source venv/bin/activate`

Installing dependencies for local env <br />
`pip install -r requirements.txt`

## Running tests

You need to install prerequesities first<br />
`pip install pytest pytest-flask`

When you have dependencies simply run:<br />
`pytest`

## Starting application

1. You need to provide api key for geolocation api.

2. Application can be started from docker compose<br />
`docker compose -f docker-compose.yaml up`



## Exposed endpoints
WARNING: IPstack free license wont allow you to query in bulk so expect error 424 if you try that.

### Add Geolocation Data to DB
Endpoint:
POST /v1/geolocation/add

Example Request Body (JSON):
```
{
  "ips": ["192.168.1.1", "10.0.0.1"],
  "domains": ["example.com", "anotherdomain.com"]
}
```

Example Response:


200 OK – Successfully processed geolocation data
```
{
  "status": "success",
  "data": [
    {
      "ip": "192.168.1.1",
      "country": "US",
      "city": "New York"
    }
  ]
}
```

Curl command for Add:
```
curl -X POST http://localhost:6622/v1/geolocation/add \
     -H "Content-Type: application/json" \
     -d '{
           "ips": ["62.33.12.56", "98.22.79.22"],
           "domains": ["google.com", "anotherdomain.com"]
         }'
```

### Get Geolocation Data
Endpoint:
GET /v1/geolocation/get?ip=<IP>

Example Request:
```
GET /v1/geolocation/get?ip=192.168.1.1
```

Example Response:

200 OK – Returns geolocation data
```
[
  {
    "city": "Pskov",
    "country": "RU",
    "hostname": "62.33.12.56",
    "id": 1,
    "ip": "62.33.12.56",
    "timestamp": "Thu, 06 Mar 2025 21:18:06 GMT"
  }
]
```

Curl command
```
curl -X GET "http://localhost:6622/v1/geolocation/get?ip=62.33.12.56" \
     -H "Content-Type: application/json"
```

Get in bulk
```
POST /v1/geolocation/add
```
Example Request Body (JSON):
```
curl -X POST http://localhost:6622/v1/geolocation/get \
     -H "Content-Type: application/json" \
     -d '{
           "ips": ["62.33.12.56", "10.0.0.1"]
         }'
```

### Delete Geolocation Data from DB

DELETE /v1/geolocation/delete

Example Request Body (JSON):
```
{
  "ips": ["192.168.1.1", "10.0.0.1"]
}
```
Example response:
```
{
  "status": "records removed"
}
```

Curl command
```
curl -X DELETE http://localhost:6622/v1/geolocation/delete \
     -H "Content-Type: application/json" \
     -d '{
           "ips": ["192.168.1.1", "10.0.0.1"]
         }'
```