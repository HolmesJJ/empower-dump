# Empower-Dump

## Folder Structure

All source files should be placed into `empower-dump` directory. The contents are as follows:

- `empower-auth` - Data files.
- `web` - Static web pages.
- `test` - Unit testing covers all endpoints in `app.py`.
- `hash.py` - Password hashing.
- `app.py` - Entry point, a Flask server contains 3 endpoints: `login`, `summary` and `rank`.
- `requirements.txt` - Required Python packages.

## APIs

### (Post) `login`: http://127.0.0.1:5000/api/login

Request
```json
{
    "username": "max",
    "password": "max"
}
```

Success Response
```json
{
    "code": 1,
    "message": "success",
    "data": {
        "id": "6099121fe5318c9103f1689f",
        "username": "max",
        "email": "",
        "first_name": "max",
        "roles": [
            "User"
        ],
        "avatar": 0,
        "gender": "male",
        "age": 1,
        "trial_id": "max",
        "is_control": false,
        "location": "Tampines Polyclinic",
        "token": {
            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NTg0NTg5NCwianRpIjoiODJmMGIxOWUtMWUzNy00YjlhLWFkYmItZjk1MWU2MjhlMjY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIiLCJuYmYiOjE2NzU4NDU4OTQsImV4cCI6MTY3NTkzMjI5NH0.XMyreCpiiYidqN16--TdWxL_6q2XeWRbjB5FxpQ2NQM",
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NTg0NTg5NCwianRpIjoiNTRmNTBkNWEtNzQyYS00ZjViLWFhZTctMTRmZjg0ZWYwMjZhIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJ1c2VyIiwibmJmIjoxNjc1ODQ1ODk0LCJleHAiOjE2Nzg0Mzc4OTR9.2Sp_EoXT2KtrKHRUij1J-e2YWjBqT4kl7HkqFP8wJYE",
            "type": "bearer",
            "expires_in": 86400
        }
    }
}
```

### (Post) `summary`: http://127.0.0.1:5000/api/summary

Authorization Required

Request
```json
{
    "id": "6099121fe5318c9103f1689f",
    "date": "2021-04-21"
}
```

Success Response
```json
{
    "code": 1,
    "message": "success",
    "data": {
        "steps": 2713,
        "distance": 1.76,
        "calories": 1364,
        "active_minutes": 25
    }
}
```


### (GET) `rank`: http://127.0.0.1:5000/api/rank

Authorization Required

Success Response
```json
{
    "code": 1,
    "message": "success",
    "data": [
        "phangjiekie",
        "epg002",
        "etp014",
        "etp022",
        "jimmya",
        "epg005",
        "etp001",
        "epg010",
        "etp013",
        "etp002",
        "epg011",
        "etp018",
        "etp021",
        "etp009",
        "etp008",
        "epg006",
        "etp007",
        "epg009",
        "etp010ah",
        "epg001",
        "epg019",
        "epg015",
        "etp011",
        "ebd003",
        "etp016",
        "etp026",
        "epg022",
        "etp024",
        "epg003",
        "epg012",
        "ebd006",
        "max",
        "etp025",
        "epg023",
        "etp003",
        "epg021",
        "epg007",
        "ebd009",
        "epg004",
        "etp034",
        "epg016",
        "ebd010",
        "epg017",
        "etp019",
        "etp033",
        "etp030",
        "etp015",
        "epg018",
        "etp032",
        "ebd001",
        "epg024",
        "epg013",
        "etp027",
        "epg025",
        "epg008",
        "ebd007",
        "etp017",
        "etp006",
        "ebd008",
        "etp012",
        "epg029",
        "ebd004",
        "epg014",
        "ebd013",
        "etp031",
        "ebd012",
        "epg020",
        "etp020",
        "ebd014",
        "etp028",
        "epg027",
        "epg026",
        "etp023",
        "epg028",
        "etp029",
        "abc",
        "ebd011",
        "ebd002",
        "etp004"
    ]
}
```

### Failed Response Format

Erroe message will be displayed in the `message` field.
```json
{
    "code": 0,
    "message": ""
}
```

## Quick Start

### Database

1. Install and start MongoDB using the following commands.
```
# Install MongoDB
brew install mongodb-community@4.4

# Start MongoDB
brew services start mongodb-community@4.4

# Stop MongoDB
brew services stop mongodb-community@4.4
```

2. Import data to MongoDB using the following commands.
```
# Import patient data
mongorestore -d empower-auth -c patient empower-auth/patient.bson

# Import daily_activity_summary data
mongorestore -d empower-auth -c daily_activity_summary empower-auth/daily_activity_summary.bson
```

### Python

1. Install Anaconda following the [link](https://docs.anaconda.com/anaconda/install/index.html).

2. Create and activate environment using the following commands.
```
# Create Python environment
conda create --name empower-auth python=3.7.10

# Check Python environment
conda info --envs

# Activate environment
conda activate empower-auth

# Deactivate environment
conda deactivate

# Remove environment
conda remove -n empower-auth --all
```

### Launch Application

Run `start.sh`.
```
./start.sh
```

### Testing

Run unit testing using the following command.
```
python -m pytest
```
