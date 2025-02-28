# Formaloo Appstore Service

This project implements a core feature for the AppStore service where users can create and manage apps, and administrators can verify them.

## Requirements
- Python 3.12
- Django 4.2

## Features
- **App Creation:** Authenticated users can create new apps via a REST API endpoint.
- **Admin Verification:** Administrators can view all apps in the Django admin panel, filter by verification status, and mark selected apps as verified.
- **Mocked Endpoints:** Signup, login, app listing, and purchase endpoints are provided as stubs.
- **API Documentation:** Swagger and Redoc documentation is available.
- **Testing:** Unit tests are written using pytest.
- **Dockerized Setup:** Run the application locally using Docker and docker-compose.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/baratihd/formaloo.git
   cd foraloo
   ```
2. **Create env file:**
   ```bash
   cp envs/.env.sample envs/.env.local
   ```
3. **Build and start the Docker containers:**
   ```bash
   docker compose up -d --build
   ```
4. **Create a superuser for the admin panel:**
   ```bash
   docker exec -it backend python manage.py createsuperuser
   ```
5. **Access the application:**
   - API base url: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/
   - API Docs (Swagger): http://localhost:8000/swagger/
   - API Docs (Redoc): http://localhost:8000/swagger/redoc/
6. **Running Tests:**
   ```bash
   docker compose run backend pytest
   ```

# Dashboard Design
Click bellow link to see **Dashboard Design** documentation.

[![**Dashboard Design**](https://img.shields.io/badge/Developer%20Documentation-orange?style=for-the-badge&logo=developer)](./docs/dashboard.md)


## Helpful commands:
- To run project (Developer):
```bash
pip install -U pip
pip install -r requirements/local.txt
```
- To format code:
```bash
./scripts/reformat
```
- To initialize pre-commit hooks:
```bash
pre-commit install
```
