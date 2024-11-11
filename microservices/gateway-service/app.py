from fastapi import FastAPI, HTTPException, Request
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.propagate import inject
import httpx
import logging

app = FastAPI()

# Base URLs of the microservices - local
AUTH_SERVICE_URL = "http://localhost:8001"
VEHICLE_SERVICE_URL = "http://localhost:8002"
BOOKING_SERVICE_URL = "http://localhost:8003"
POST_SALE_SERVICE_URL = "http://localhost:8004"
ROADSIDE_ASSISTANCE_URL = "http://localhost:8005"
CUSTOMER_FEEDBACK_URL = "http://localhost:8006"
CUSTOMER_SERVICE_URL = "http://localhost:8007"

# Base URLs of the microservices - Kubernetes Service names
# AUTH_SERVICE_URL = "http://auth-svc"
# VEHICLE_SERVICE_URL = "http://vehicle-svc"
# BOOKING_SERVICE_URL = "http://booking-svc"
# POST_SALE_SERVICE_URL = "http://support-svc"
# ROADSIDE_ASSISTANCE_URL = "http://rsa-svc"
# CUSTOMER_FEEDBACK_URL = "http://feedback-svc"
# CUSTOMER_SERVICE_URL = "http://customer-svc"

# ===========================
# OpenTelemetry and Jaeger Setup
# ===========================
def configure_opentelemetry():
    resource = Resource(attributes={
        "service.name": "fastapi-service",
        "service.version": "1.0.0"
    })

    trace.set_tracer_provider(TracerProvider(resource=resource))

    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=6831,
    )

    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    console_exporter = ConsoleSpanExporter()
    trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(console_exporter))

configure_opentelemetry()
FastAPIInstrumentor.instrument_app(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

from fastapi import Request
import httpx
import logging

logging.basicConfig(level=logging.DEBUG)


async def forward_request(service_url: str, request: Request):
    async with httpx.AsyncClient() as client:
        headers = dict(request.headers)

        # Inject the trace context into the headers (adds traceparent for propagation)
        inject(headers)

        # Forward the request to the downstream service
        response = await client.request(
            method=request.method,
            url=service_url + request.url.path,
            headers=headers,
            json=await request.json() if request.method in ["POST", "PUT"] else None,
            params=request.query_params if request.method == "GET" else None,
        )
        return response.json()

# async def forward_request(service_url: str, request: Request):
#     try:
#         headers = dict(request.headers)
#
#         # Only inject headers if needed, without affecting Content-Length
#         inject(headers)
#
#         # Prepare request data
#         request_data = None
#         if request.method in ["POST", "PUT"]:
#             request_data = await request.json()
#
#         # Log headers and payload size for debugging
#         logging.debug(f"Forwarding request to {service_url + request.url.path}")
#         logging.debug(f"Headers: {headers}")
#         logging.debug(f"Payload size: {len(str(request_data)) if request_data else 'N/A'}")
#
#         # Forward the request to the service
#         async with httpx.AsyncClient() as client:
#             response = await client.request(
#                 method=request.method,
#                 url=service_url + request.url.path,
#                 headers=headers,
#                 json=request_data if request_data else None,  # Pass JSON only if it exists
#                 params=request.query_params if request.method == "GET" else None
#             )
#             response.raise_for_status()
#
#         # Return response JSON from downstream service
#         return response.json()
#
#     except httpx.HTTPStatusError as exc:
#         logging.error(f"HTTP error from downstream: {exc.response.status_code} - {exc.response.text}")
#         raise HTTPException(status_code=exc.response.status_code, detail="Error from downstream service")
#     except Exception as e:
#         logging.error(f"An error occurred: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# Ping API
@app.get("/ping")
def ping():
    return {"msg": "pong-gateway-svc"}

# Auth Service APIs
# Auth Service APIs
@app.post("/auth/register")
async def register_user(request: Request):
    try:
        request_data = await request.json()
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{AUTH_SERVICE_URL}/auth/register", json=request_data)
            response.raise_for_status()  # Raises an error for 4xx/5xx responses
        return response.json()
    except httpx.HTTPStatusError as exc:
        logging.error(f"HTTP error during registration: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        logging.error(f"Error processing registration request: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid input data")


@app.post("/auth/login")
async def login_for_access_token(request: Request):
    try:
        request_data = await request.json()
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{AUTH_SERVICE_URL}/login", json=request_data)
            response.raise_for_status()  # Raises an error for 4xx/5xx responses
        return response.json()
    except httpx.HTTPStatusError as exc:
        logging.error(f"HTTP error during login: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        logging.error(f"Error processing login request: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid input data")


# Customer Service APIs
@app.get("/customers")
async def get_all_customers(request: Request):
    return await forward_request(CUSTOMER_SERVICE_URL, request)

@app.get("/customers/{customer_id}")
async def get_customer_by_id(customer_id: str, request: Request):
    return await forward_request(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}", request)

@app.delete("/customers/{customer_id}")
async def delete_customer_by_id(customer_id: str, request: Request):
    return await forward_request(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}", request)

@app.post("/customers")
async def create_customer(request: Request):
    try:
        request_data = await request.json()
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{CUSTOMER_SERVICE_URL}/customers", json=request_data)
            response.raise_for_status()  # Raises an error for 4xx/5xx responses
        return response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid input data")


# Vehicle Service APIs
# Vehicle Service APIs
@app.post("/vehicles")
async def create_vehicle(request: Request):
    try:
        request_data = await request.json()  # Get the request body as JSON
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{VEHICLE_SERVICE_URL}/vehicles", json=request_data)
            response.raise_for_status()  # Raises an error for 4xx/5xx responses
        return response.json()  # Return the response from the vehicle service
    except httpx.HTTPStatusError as exc:
        logging.error(f"HTTP error during vehicle creation: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        logging.error(f"Error processing vehicle creation request: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid input data")


@app.get("/vehicles")
async def get_vehicles(request: Request):
    return await forward_request(VEHICLE_SERVICE_URL, request)

@app.get("/vehicles/{vehicle_id}")
async def get_vehicle_by_id(vehicle_id: str, request: Request):
    return await forward_request(f"{VEHICLE_SERVICE_URL}/vehicles/{vehicle_id}", request)

# Booking Service APIs
@app.get("/testdrives")
async def get_test_drives(request: Request):
    return await forward_request(BOOKING_SERVICE_URL, request)


@app.post("/testdrives/book", status_code=201)
async def book_test_drive(request: Request):
    try:
        request_data = await request.json()  # Get the request body as JSON
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BOOKING_SERVICE_URL}/testdrives/book", json=request_data)
            response.raise_for_status()  # Raises an error for 4xx/5xx responses
        return response.json()  # Return the response from the post-sale service
    except httpx.HTTPStatusError as exc:
        logging.error(f"HTTP error during service scheduling: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        logging.error(f"Error processing service scheduling request: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid input data")


@app.get("/vehicles/{test_drive_id}")
async def get_testdrives_by_id(test_drive_id: str, request: Request):
    return await forward_request(f"{BOOKING_SERVICE_URL}/testdrives/{test_drive_id}", request)



# Post-Sale Service APIs
# Post-Sale Service APIs
@app.post("/service/schedule")
async def schedule_service(request: Request):
    try:
        request_data = await request.json()  # Get the request body as JSON
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{POST_SALE_SERVICE_URL}/service/schedule", json=request_data)
            response.raise_for_status()  # Raises an error for 4xx/5xx responses
        return response.json()  # Return the response from the post-sale service
    except httpx.HTTPStatusError as exc:
        logging.error(f"HTTP error during service scheduling: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        logging.error(f"Error processing service scheduling request: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid input data")


@app.get("/service/history")
async def get_service_history(request: Request):
    return await forward_request(POST_SALE_SERVICE_URL, request)

@app.get("/service/appointments")
async def get_service_appointments(request: Request):
    return await forward_request(POST_SALE_SERVICE_URL, request)

# Roadside Assistance Service APIs
@app.post("/rsa/requests")
async def request_roadside_assistance(request: Request):
    return await forward_request(ROADSIDE_ASSISTANCE_URL, request)

# Roadside Assistance Service APIs
@app.get("/rsa/requests")
async def get_roadside_status(request: Request):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ROADSIDE_ASSISTANCE_URL}/rsa/requests", headers=dict(request.headers))
            response.raise_for_status()  # Raises an error for 4xx/5xx responses
        return response.json()  # Return the response from the roadside assistance service
    except httpx.HTTPStatusError as exc:
        logging.error(f"HTTP error while fetching roadside assistance status: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        logging.error(f"Error processing roadside assistance status request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/rsa/requests/{requestId}")
async def get_roadside_request_by_id(requestId: str, request: Request):
    return await forward_request(f"{ROADSIDE_ASSISTANCE_URL}/rsa/requests/{requestId}", request)

# Customer Feedback Service APIs
@app.post("/feedback/submit")
async def submit_feedback(request: Request):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{CUSTOMER_FEEDBACK_URL}/feedback/submit", headers=dict(request.headers), json=await request.json())
            response.raise_for_status()  # Raises an error for 4xx/5xx responses
        return response.json()  # Return the response from the customer feedback service
    except httpx.HTTPStatusError as exc:
        logging.error(f"HTTP error while submitting feedback: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        logging.error(f"Error processing feedback submission: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/feedback/{id}")
async def get_feedback_by_id(id: str, request: Request):
    return await forward_request(f"{CUSTOMER_FEEDBACK_URL}/feedback/{id}", request)
