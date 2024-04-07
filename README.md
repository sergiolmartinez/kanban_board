# Django REST Framework Project

This project is a RESTful API built with Django REST Framework (DRF). It includes a tasks management system with CRUD operations.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- pip
- Virtual environment

### Setting Up a Development Environment

1. Clone the repository:

```bash
git clone <repository-url>
```

2. Navigate to the project directory:

```bash
cd <project-directory>
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment:

- On macOS and Linux:

```bash
source venv/bin/activate
```

- On Windows:

```bash
.\venv\Scripts\activate
```

5. Install the dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables

To run the project, you need to set up the following environment variables. Create a `.env` file in the root directory of the project and add the following lines:

```plaintext
DATABASE_USER=postgres
DATABASE_PASSWORD=<YourDatabasePassword>
DATABASE_PORT=5432
SECRET_KEY=<YourSecretKey>
```

**Note:** Replace `<YourDatabasePassword>` and `<YourSecretKey>` with your actual PostgreSQL database password and Django secret key, respectively. **Do not share your `.env` file or include your real credentials in any public repository.**

### Database Setup

Make sure PostgreSQL is installed and running on your machine. Create a database for the project and ensure the `DATABASE_USER` and `DATABASE_PASSWORD` in your `.env` file have the necessary permissions.

### Running the Development Server

Once the environment variables are set and the database is ready, you can run the development server:

```bash
python manage.py runserver
```

This will start the server on `http://127.0.0.1:8000/`, where you can access the API endpoints.
