# **Vehicle Management System API**

## Vehicle Retrieval

### Get Vehicle List

**Endpoint:** `/vehicle`

**Method:** `GET`

**Description:** This endpoint retrieves a list of vehicles available in the system.

**Response Schema:**

```json
[
  {
    "id": "string",
    "make": "string",
    "model": "string",
    "year": "integer",
    "price": "integer",
    "fuel_type": "string",
    "transmission": "string",
    "body_type": "string",
    "image_url": "string"
  }
]
```

**Example Response:**

```json
[
  {
    "id": "b9d916a6",
    "make": "Toyota",
    "model": "Camry",
    "year": 2021,
    "price": 24000,
    "fuel_type": "Gasoline",
    "transmission": "Automatic",
    "body_type": "Sedan",
    "image_url": "http://example.com/toyota_camry.jpg"
  }
]
```

### Get Vehicle Details

**Endpoint:** `/vehicles/{id}`

**Method:** `GET`

**Description:** This endpoint retrieves the details of a specific vehicle by its ID.

**Response Schema:**

```json
{
  "id": "string",
  "make": "string",
  "model": "string",
  "year": "integer",
  "price": "integer",
  "fuel_type": "string",
  "transmission": "string",
  "body_type": "string",
  "image_url": "string"
}
```

**Example Response:**

```json
{
  "id": "b9d916a6",
  "make": "Toyota",
  "model": "Camry",
  "year": 2021,
  "price": 24000,
  "fuel_type": "Gasoline",
  "transmission": "Automatic",
  "body_type": "Sedan",
  "image_url": "http://example.com/toyota_camry.jpg"
}
```
