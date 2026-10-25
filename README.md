# SlowAPI

A small Python backend framework built from scratch to understand how web frameworks work under the hood.

SlowAPI is an educational project that implements a lightweight routing layer on top of **WSGI**. The project explores request handling, route registration, middleware, dynamic URL parameters, response objects, class-based routes, query-string parsing, and a basic HTML template renderer.

> **Status:** Learning project. This is not intended to be a production-ready replacement for Flask, FastAPI, or Django.

## Features

- **WSGI application interface** compatible with servers such as Gunicorn.
- **Decorator-based routing** for HTTP methods such as `GET` and `POST`.
- **Route registration** with method-specific handlers.
- **Default 404 responses** for unknown routes.
- **Dynamic URL parameters** using route patterns and the `parse` package.
- **Global middleware** that runs before route handling.
- **Route-specific middleware** for individual endpoints.
- **Class-based routing** for organizing handlers by HTTP method.
- **Request object** for accessing request information and query parameters.
- **Response object** with a `send()` method and WSGI response handling.
- **Basic HTML template rendering** with context-value substitution.

## How it works

At a high level, a request travels through the following flow:

1. A client sends an HTTP request.
2. A WSGI server, such as Gunicorn, receives the request.
3. Gunicorn calls the SlowAPI application with the WSGI `environ` dictionary and `start_response` callable.
4. SlowAPI runs the configured middleware.
5. The router matches the request path and HTTP method.
6. SlowAPI invokes the matching handler and provides request/response objects.
7. The response is converted into a WSGI-compatible response and returned to the server.
8. The server sends the response back to the client.

### WSGI

WSGI stands for **Web Server Gateway Interface**. It defines a standard interface between a Python web application and a compatible web server.

A WSGI application is a callable that receives:

- `environ`: a dictionary containing request and server information.
- `start_response`: a callable used to provide the HTTP status and response headers.

The application returns an iterable containing the response body as bytes.

## Project structure

The project is organized around these modules. Adjust the names below if your repository uses a different layout.

```text
.
├── main.py        # SlowAPI application and routing logic
├── request.py     # Request abstraction and query-string parsing
├── response.py    # Response handling, send(), and template rendering
├── example.py     # Example application built with SlowAPI
├── templates/     # HTML templates used by render()
└── README.md
```

## Requirements

- Python 3
- Gunicorn
- `parse`

Gunicorn is commonly used on Linux environments. On Windows, run the project through **WSL** or another compatible Linux environment rather than trying to run Gunicorn natively.

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

Replace the placeholders with your repository URL and directory name.

### 2. Create a virtual environment

Using a virtual environment keeps this project's dependencies separate from other Python projects. Humans have somehow made dependency conflicts a recurring hobby, so this step is worth doing.

```bash
python3 -m venv .venv
```

Activate it on Linux or WSL:

```bash
source .venv/bin/activate
```

On Windows PowerShell, if running a compatible local workflow:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install gunicorn parse
```

If the repository has a `requirements.txt`, install from it instead:

```bash
python -m pip install -r requirements.txt
```

## Running the example

If `example.py` creates an application instance named `slow`, run:

```bash
gunicorn example:slow
```

The format is `gunicorn module_name:application_object`. In this example, Gunicorn imports `example.py` and loads the `slow` application instance.

Gunicorn must be able to import the module from the current environment and working directory.

## Usage

The following examples illustrate the intended API described by this project. Match the imports and exact method signatures to the current source code in the repository.

### Create an application

```python
from main import SlowAPI

slow = SlowAPI()
```

The implementation notes use the class name `slowapi`; Python is case-sensitive, so use the exact class name defined in your code. If the class is named `slowapi`, initialize it like this:

```python
from main import slowapi

slow = slowapi()
```

### Register a route

A route decorator associates a URL path and HTTP method with a handler function.

```python
@slow.get("/users")
def get_users(req, res):
    res.send(["Rivaan", "Shivang"])
```

A handler receives the request and response abstractions. The response's `send()` method is responsible for preparing the response instead of requiring every handler to manually call WSGI's `start_response`.

### Register a POST route

```python
@slow.post("/users")
def create_user(req, res):
    res.send("User created", status_code=201)
```

The status-code argument shown here reflects the intended API. Check the implementation for the current parameter order and defaults.

### Dynamic URL parameters

Dynamic routes allow a handler to receive values extracted from the URL.

Conceptually, a route might look like:

```python
@slow.get("/users/{id}")
def get_user(req, res, id):
    res.send(f"User ID: {id}")
```

The project uses the `parse` package to match route patterns and extract values. The exact placeholder syntax supported by the current router depends on how the pattern is defined in the source code.

### Middleware

Global middleware is configured when the application is initialized. It runs before route handlers.

```python
def global_middleware(req):
    print("Request received")

slow = slowapi(middleware=[global_middleware])
```

Route-specific middleware can be attached to an individual route, if supported by the current decorator signature.

Middleware functions should follow the argument convention expected by the implementation. The project notes describe middleware receiving request/environment information and validating that each middleware entry is callable.

### Class-based routing

Class-based routing groups HTTP method handlers into a class, keeping related endpoints together. The router identifies supported method handlers and registers them for the route.

Use the exact route decorator and class signature implemented in the repository when writing an example, since this API is still being developed.

### Query parameters

The request abstraction parses query strings into a dictionary-like structure. For example, a request to:

```text
/users?id=123&name=Rivaan
```

contains query parameters equivalent to:

```python
{
    "id": "123",
    "name": "Rivaan"
}
```

Query parameter values are generally strings unless the application converts them.

### Render an HTML template

The response abstraction includes a basic `render()` method intended to load an HTML template and substitute values from a context dictionary.

For example, a template might contain:

```html
<h1>Hello, {{name}}</h1>
<p>{{message}}</p>
```

The handler can pass values such as `name` and `message` to the renderer. This is a minimal educational template system, not a full template engine. Do not use it with untrusted template content without reviewing its implementation and escaping behavior.

## Concepts explored

This project is also a practical way to study:

- WSGI application callables
- Python callable classes and `__call__`
- Decorators and nested wrapper functions
- Route registration and handler lookup
- HTTP methods and status codes
- Request and response abstractions
- Middleware execution
- Dynamic route matching
- Query-string parsing
- Class-based views
- Template rendering and regular expressions

## Current limitations

Based on the current development notes:

- The framework is still under development and may have incomplete edge-case handling.
- The routing API and supported HTTP methods may change.
- The template renderer is intentionally minimal.
- Request-body parsing, robust error handling, and production security features are not documented as complete.
- Middleware and class-based routing APIs should be checked against the current source before relying on these examples.
- This project has not been presented as production-tested.

## Learning references

- [Python WSGI specification (PEP 3333)](https://peps.python.org/pep-3333/)
- [Gunicorn documentation](https://docs.gunicorn.org/)
- [The `parse` package](https://pypi.org/project/parse/)
- [Middleware tutorial referenced during development](https://youtu.be/Lb-5ziwsqpc)

## Contributing

This is a learning project. Bug reports, clearer examples, and improvements to routing, middleware, response handling, and tests are useful contributions.

## License

No license has been specified yet. Add a `LICENSE` file before presenting the project as open source.
