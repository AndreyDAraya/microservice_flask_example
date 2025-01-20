# User Management API

A RESTful API for user management implemented with Flask and hexagonal architecture.

## 🏗 Architecture

The project follows a hexagonal (ports & adapters) architecture with the following layers:

- **Core**: Contains domain entities and ports (interfaces)
  - Domain entities like `User` with rich domain logic
  - Repository interfaces defining persistence contracts
- **Application**: Houses use cases implementing business logic
  - CRUD operations for users
  - Password management
  - User status management
- **Infrastructure**: Concrete implementations
  - SQLAlchemy repository implementations
  - Database models and configurations
- **Interfaces**: REST APIs and controllers
  - Flask controllers handling HTTP requests
  - Request/Response DTOs

## 🚀 Features

- Complete user CRUD operations
- JWT Authentication
- Swagger Documentation
- Unit Tests with pytest
- PostgreSQL Database
- Docker Compose for development
- Database migrations with Alembic

## 📋 Requirements

- Python 3.8+
- Docker and Docker Compose
- PostgreSQL

## 🛠 Installation

1. Clone the repository:

```bash
git clone https://github.com/AndreyDAraya/microservice_flask_example.git
cd microservice_flask_example
```

2. Create virtual environment:

```bash
python3 -m venv venv
```

3. Activate virtual environment:

For bash/zsh:

```bash
. venv/bin/activate  # Note the dot at the start
```

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

For Windows CMD:

```cmd
.\venv\Scripts\activate.bat
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Start database with Docker Compose:

```bash
docker-compose up -d
```

6. Run migrations:

```bash
alembic upgrade head
```

7. Run the application:

```bash
FLASK_RUN_PORT=8000 python -m flask run
```

## 🧪 Tests

Run unit tests:

```bash
pytest
```

## 📚 API Documentation

Swagger documentation is available at:

```
http://localhost:8000/docs/
```

## 🔑 Endpoints

### Authentication

- POST `/api/v1/auth/login`: Login and obtain JWT token

### Users

- POST `/api/v1/users`: Create user
  - Request body: email, password, first_name, last_name
  - Returns: Created user object
- GET `/api/v1/users`: List users
  - Returns: Array of user objects
- GET `/api/v1/users/{id}`: Get user by ID
  - Returns: User object
- PUT `/api/v1/users/{id}`: Update user
  - Request body: first_name, last_name
  - Returns: Updated user object
- DELETE `/api/v1/users/{id}`: Delete user
  - Returns: Success boolean

## 🏗 Project Structure

```
.
├── migrations/               # Alembic migrations
│   ├── versions/            # Migration files
│   ├── alembic.ini         # Alembic config
│   ├── env.py              # Migration environment
│   └── script.py.mako      # Migration template
├── src/
│   ├── core/               # Domain layer
│   │   ├── entities/       # Domain entities
│   │   │   └── user.py     # User entity with domain logic
│   │   └── ports/          # Interfaces/ports
│   │       └── user_repository.py
│   ├── application/        # Use cases
│   │   └── use_cases/
│   │       └── user_use_cases.py
│   ├── infrastructure/     # Implementations
│   │   ├── database/
│   │   │   └── models.py  # SQLAlchemy models
│   │   └── repositories/
│   │       └── sqlalchemy_user_repository.py
│   ├── interfaces/         # APIs and controllers
│   │   └── rest/
│   │       └── controllers.py
│   ├── app.py             # Entry point
│   └── config.py          # Configuration
├── tests/                 # Tests
│   └── unit/
│       └── test_user_use_cases.py
├── .env                   # Environment variables
├── docker-compose.yml     # Docker configuration
├── pytest.ini            # pytest configuration
└── requirements.txt      # Dependencies
```

## 🔒 Environment Variables

Create a `.env` file with:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://admin:admin123@localhost:5432/users_db
```

## 📦 Database and Migrations

### Database Connection

PostgreSQL database runs in a Docker container and is available for external connections with:

- **Host**: localhost
- **Port**: 5432
- **Database**: users_db
- **User**: admin
- **Password**: admin123
- **Connection URL**: `postgresql://admin:admin123@localhost:5432/users_db`

To connect using DataGrip or similar tools:

1. Ensure Docker container is running (`docker-compose up -d`)
2. Use above credentials to configure a new connection
3. Container exposes port 5432, connect as if it were a local PostgreSQL instance

### Migration Management

The project uses Alembic for database migrations:

- Create new migration:

```bash
alembic revision --autogenerate -m "change description"
```

- Apply pending migrations:

```bash
alembic upgrade head
```

- Revert last migration:

```bash
alembic downgrade -1
```

## 🔧 Technical Implementation Details

### Domain Model

The User entity (`src/core/entities/user.py`) implements rich domain logic:

- Password management with `update_password()`
- User status management with `activate()` and `deactivate()`
- Profile updates with `update_profile()`
- Automatic timestamp management for created_at/updated_at

### Use Cases

The UserUseCases class (`src/application/use_cases/user_use_cases.py`) implements:

- User creation with email uniqueness validation
- Profile updates maintaining data consistency
- Password changes with proper state management
- User status toggling (activate/deactivate)
- CRUD operations with proper error handling

### Repository Pattern

The UserRepository interface (`src/core/ports/user_repository.py`) defines:

- Basic CRUD operations
- Email existence checking
- Clear contracts for infrastructure implementations

## 👥 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is under the MIT License.
