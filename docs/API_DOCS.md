# REST API Documentation
## Smart Online Examination & Learning Analytics System

All API endpoints are versioned under `/api/v1/` and protected with session/token authentication.

### Interactive OpenAPI Documentation
- **Swagger UI**: `http://127.0.0.1:8000/api/docs/`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/`
- **OpenAPI 3.0 Schema**: `http://127.0.0.1:8000/api/schema/`

### Core Endpoints Table
| Endpoint | HTTP Method | Description |
| :--- | :--- | :--- |
| `/api/v1/users/` | GET | List user accounts (Admin) |
| `/api/v1/departments/` | GET, POST, PUT, DELETE | Department management |
| `/api/v1/courses/` | GET, POST, PUT, DELETE | Course management |
| `/api/v1/subjects/` | GET, POST, PUT, DELETE | Subject management |
| `/api/v1/questions/` | GET, POST, PUT, DELETE | Question Bank CRUD |
| `/api/v1/exams/` | GET, POST, PUT, DELETE | Exam configurations |
| `/api/v1/attempts/` | GET, POST | Exam attempt records |
| `/api/v1/certificates/` | GET | Earned certificate metadata |
| `/api/v1/notifications/` | GET | Unread notifications |
