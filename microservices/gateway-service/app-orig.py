from fastapi import FastAPI, HTTPException, Request
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.propagate import inject, extract

import httpx

app = FastAPI()

#Base URLs of the microservices
AUTH_SERVICE_URL = "http://localhost:8001"
VEHICLE_SERVICE_URL = "http://localhost:8002"
BOOKING_SERVICE_URL = "http://localhost:8003"
POST_SALE_SERVICE_URL = "http://localhost:8004"
ROADSIDE_ASSISTANCE_URL = "http://localhost:8005"
CUSTOMER_FEEDBACK_URL = "http://localhost:8006"
CUSTOMER_SERVICE_URL = "http://localhost:8007"

# Base URLs of the microservices with Kubernetes Service names
# AUTH_SERVICE_URL = "http://auth-svc"
# VEHICLE_SERVICE_URL = "http://vehicle-svc"
# BOOKING_SERVICE_URL = "http://booking-svc"
# POST_SALE_SERVICE_URL = "http://support-svc"
# ROADSIDE_ASSISTANCE_URL = "http://rsa-svc"
# CUSTOMER_FEEDBACK_URL = "http://feedback-svc"
# CUSTOMER_SERVICE_URL = "http://customer-svc"


# ===========================
# OpenTelemetry and Jaeger Setup`
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

#Function to handle requests and forward them to the appropriate service
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
#     async with httpx.AsyncClient() as client:
#         headers = dict(request.headers)
#
#         # Inject the trace context into the headers (adds traceparent for propagation)
#         inject(headers)
#
#         try:
#             request_json = await request.json() if request.method in ["POST", "PUT"] else None
#             response = await client.request(
#                 method=request.method,
#                 url=service_url + request.url.path,
#                 headers=headers,
#                 json=request_json,
#                 params=request.query_params if request.method == "GET" else None,
#             )
#             response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
#             return response.json()
#         except httpx.HTTPStatusError as e:
#             # Log the error and the response for further investigation
#             print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
#             raise
#         except Exception as e:
#             # Log any other exceptions
#             print(f"An error occurred: {str(e)}")
#             raise


#Ping APIs
@app.get("/ping")
def ping():
    return {"msg": "pong-gateway-svc"}


# Auth Service APIs
@app.post("/auth/register")
async def register_user(request: Request):
    return await forward_request(AUTH_SERVICE_URL, request)

@app.post("/auth/login")
async def login_for_access_token(request: Request):
    return await forward_request(AUTH_SERVICE_URL, request)

# Customer Service APIs
@app.get("/customers")
async def get_all_customers(request: Request):
    return await forward_request(CUSTOMER_SERVICE_URL, request)


@app.get("/customers/{customer_id}")
async def get_customer_by_id(customer_id: str, request: Request):
    async with httpx.AsyncClient() as client:
        headers = dict(request.headers)

        # Inject the trace context into the headers (adds traceparent for propagation)
        inject(headers)

        # Call the downstream service directly
        url = f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}"
        response = await client.get(url, headers=headers)

        # Check the response status and return the appropriate result
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Customer not found")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from downstream service")

@app.delete("/customers/{customer_id}")
async def delete_customer_by_id(customer_id: str, request: Request):
    async with httpx.AsyncClient() as client:
        headers = dict(request.headers)

        # Inject the trace context into the headers (adds traceparent for propagation)
        inject(headers)

        # Call the downstream service directly with DELETE method
        url = f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}"
        response = await client.delete(url, headers=headers)

        # Check the response status and return the appropriate result
        if response.status_code == 204:  # No Content response for successful delete
            return {"detail": "Customer deleted successfully"}
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Customer not found")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from downstream service")


@app.post("/customers")
async def create_customer(request: Request):
    return await forward_request(CUSTOMER_SERVICE_URL, request)

# Vehicle Service APIs
@app.post("/vehicles")
async def create_customer(request: Request):
    return await forward_request(VEHICLE_SERVICE_URL, request)

@app.get("/vehicles")
async def get_vehicles(request: Request):
    return await forward_request(VEHICLE_SERVICE_URL, request)

@app.get("/vehicles/{vehicle_id}")
async def get_vehicle_by_id(vehicle_id: str, request: Request):
    async with httpx.AsyncClient() as client:
        headers = dict(request.headers)

        # Inject the trace context into the headers (adds traceparent for propagation)
        inject(headers)

        # Call the downstream service directly
        url = f"{VEHICLE_SERVICE_URL}/vehicles/{vehicle_id}"
        response = await client.get(url, headers=headers)

        # Check the response status and return the appropriate result
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Customer not found")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from downstream service")
# @app.put("/vehicles/{vehicle_id}")
#
# @app.delete("/vehicles/{vehicle_id}")

# Booking Service APIs
@app.get("/testdrives")
async def get_test_drives(request: Request):
    return await forward_request(BOOKING_SERVICE_URL, request)

# Post-Sale Service APIs
@app.post("/service/schedule")
async def schedule_service(request: Request):
    return await forward_request(POST_SALE_SERVICE_URL, request)

@app.get("/service/history")
async def get_service_history(request: Request):
    return await forward_request(POST_SALE_SERVICE_URL, request)

@app.get("/service/appointments")
async def get_service_history(request: Request):
    return await forward_request(POST_SALE_SERVICE_URL, request)

# Roadside Assistance Service APIs
@app.post("/rsa/requests")
async def request_roadside_assistance(request: Request):
    return await forward_request(f"{ROADSIDE_ASSISTANCE_URL}", request)

@app.get("/rsa/requests")
async def get_roadside_status(requestId: str, request: Request):
    return await forward_request(f"{ROADSIDE_ASSISTANCE_URL}", request)

@app.get("/rsa/requests/{requestId}")
async def get_roadside_status(requestId: str, request: Request):
    async with httpx.AsyncClient() as client:
        headers = dict(request.headers)

        # Inject the trace context into the headers (adds traceparent for propagation)
        inject(headers)

        # Call the downstream service directly using GET method
        url = f"{ROADSIDE_ASSISTANCE_URL}/rsa/requests/{requestId}"
        response = await client.get(url, headers=headers)

        # Check the response status and return the appropriate result
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Roadside request not found")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from downstream service")

# Customer Feedback Service APIs
@app.post("/feedback/submit")
async def submit_feedback(request: Request):
    return await forward_request(CUSTOMER_FEEDBACK_URL, request)

@app.get("/feedback/{id}")
async def get_feedback_by_id(id: str, request: Request):
    async with httpx.AsyncClient() as client:
        headers = dict(request.headers)

        # Inject the trace context into the headers (adds traceparent for propagation)
        inject(headers)

        # Call the downstream service directly
        url = f"{CUSTOMER_FEEDBACK_URL}/feedback/{id}"
        response = await client.get(url, headers=headers)

        # Check the response status and return the appropriate result
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Customer feedback not found")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from downstream service")


# Booking Service APIs

@app.post("/bookings")
async def create_booking(request: Request):
    return await forward_request(BOOKING_SERVICE_URL, request)

@app.get("/bookings")
async def get_all_bookings(request: Request):
    return await forward_request(BOOKING_SERVICE_URL, request)

@app.get("/bookings/{booking_id}")
async def get_booking_by_id(booking_id: str, request: Request):
    async with httpx.AsyncClient() as client:
        headers = dict(request.headers)

        # Inject the trace context into the headers (adds traceparent for propagation)
        inject(headers)

        # Call the downstream service directly
        url = f"{BOOKING_SERVICE_URL}/bookings/{booking_id}"
        response = await client.get(url, headers=headers)

        # Check the response status and return the appropriate result
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Booking not found")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from downstream service")

@app.put("/bookings/{booking_id}")
async def update_booking(booking_id: str, request: Request):
    return await forward_request(f"{BOOKING_SERVICE_URL}/bookings/{booking_id}", request)

@app.delete("/bookings/{booking_id}")
async def delete_booking(booking_id: str, request: Request):
    async with httpx.AsyncClient() as client:
        headers = dict(request.headers)

        # Inject the trace context into the headers (adds traceparent for propagation)
        inject(headers)

        # Call the downstream service directly with DELETE method
        url = f"{BOOKING_SERVICE_URL}/bookings/{booking_id}"
        response = await client.delete(url, headers=headers)

        # Check the response status and return the appropriate result
        if response.status_code == 204:  # No Content response for successful delete
            return {"detail": "Booking deleted successfully"}
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Booking not found")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from downstream service")

# import httpx
# from fastapi import FastAPI, Request
#
# app = FastAPI()
#
# CUSTOMER_SERVICE_URL = "http://localhost:8007/customers"  # Replace with actual target endpoint
#
# @app.post("/customers")
# async def create_customer(request: Request):
#     async with httpx.AsyncClient() as client:
#         payload = await request.json()  # Retrieve JSON from the request
#         response = await client.post(
#             CUSTOMER_SERVICE_URL,
#             json=payload  # Use json= to let httpx handle serialization
#         )
#     return response.json()
