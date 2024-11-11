# **API Endpoints**

## Users Authentication

### User Registration

**Endpoint:** `/auth/register`

**Method:** `POST`

**Request Body:**

```json
{
  "userName": "string",
  "email": "string",
  "password": "string",
  "firstName": "string",
  "lastName": "string",
  "phoneNumber": "string",
  "address": "string"
}
```

**Response:**

```json
{
  "msg": "User registered successfully",
  "user": {
    "userName": "Username",
    "email": "email"
  }
}
```

### User Login

**Endpoint:** `/auth/login`

**Method:** `POST`

**Request Body:**

```json
{
  "userName": "string",
  "password": "string"
}
```

**Response:**

```json
{
  "msg": "Login successful",
  "user": {
    "userName": "string",
    "email": "string"
  }
}
```
