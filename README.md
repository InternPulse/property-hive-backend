# Property Hive Backend API

## Project Overview

Property Hive is a comprehensive real estate platform backend API built with Django REST Framework. The platform enables property companies to list properties, manage customers, handle transactions, and provides a complete property management solution.

**Live API:** [Property Hive API](https://api.propertyhive.com.ng/)
**API Documentation:** [Postman Collection](https://documenter.getpostman.com/view/34635068/2sAXqzVxVn)

## Features

- **User Management**: Customer and Company registration/authentication
- **Property Management**: CRUD operations for properties with images and documents
- **Transaction Processing**: Payment handling and invoice generation
- **KYC Verification**: Document upload and verification system
- **Rating System**: Property and company ratings
- **Profile Management**: Company profiles with social media integration
- **Email Verification**: Secure email verification system
- **JWT Authentication**: Token-based authentication with refresh tokens

## Tech Stack

- **Framework**: Django 5.1.1 + Django REST Framework 3.15.2
- **Database**: PostgreSQL (with psycopg2-binary)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **File Storage**: Django Media Files
- **Email**: SMTP with Gmail
- **Deployment**: Vercel (configured)
- **Other**: CORS headers, Whitenoise for static files

## Installation Instructions

### Prerequisites

Before setting up the project locally, ensure you have the following installed:

- **Python** (>=3.8)
- **PostgreSQL** (or your preferred database)
- **pip** (Python package manager)
- **Git**

### Local Development Setup

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/property-hive-backend.git
cd property-hive-backend
```

2. **Create and activate virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:

```env
SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=postgresql://username:password@localhost:5432/property_hive_db
```

5. **Database setup:**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. **Run the development server:**

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication

- `POST /api/v1/login/` - JWT Token generation
- `POST /api/v1/login/company` - Company login
- `POST /api/v1/login/customer` - Customer login
- `POST /api/v1/register/company/` - Company registration
- `POST /api/v1/register/customer` - Customer registration
- `POST /api/v1/forgot-password/` - Password reset request
- `POST /api/v1/reset-password/` - Password reset
- `POST /api/v1/send-verification-email/` - Send verification email
- `POST /api/v1/verify-email/` - Email verification

### User Management

- `GET /api/v1/profile/` - User profile

### Additional Endpoints

- Company management endpoints
- Transaction processing endpoints
- Property CRUD operations
- Media file handling

## Project Structure

```
property_hive/
├── api/v1/
│   ├── common/          # Shared models (User, Property, etc.)
│   ├── custom_auth/     # Authentication views and URLs
│   ├── company/         # Company-specific functionality
│   └── transaction/     # Transaction management
├── property_hive/       # Django project settings
├── media/              # User uploaded files
├── requirements.txt    # Python dependencies
├── manage.py          # Django management script
└── vercel.json        # Vercel deployment config
```

## Environment Variables

| Variable       | Description                  | Required |
| -------------- | ---------------------------- | -------- |
| `SECRET_KEY`   | Django secret key            | Yes      |
| `DEBUG`        | Debug mode (True/False)      | No       |
| `DATABASE_URL` | PostgreSQL connection string | Yes      |

## Deployment

The project is configured for deployment on Vercel with the included `vercel.json` configuration.

### Vercel Deployment

1. Install Vercel CLI: `npm i -g vercel`
2. Deploy: `vercel --prod`
3. Set environment variables in Vercel dashboard

## Contributing

### Branches

- **main** -> Production branch (protected)
- **dev** -> Development branch (create PRs here)

### Contribution Workflow

1. **Fork and clone:**

```bash
git clone https://github.com/your-username/property-hive-backend.git
cd property-hive-backend
```

2. **Set up development environment:**

```bash
git remote add origin https://github.com/your-username/property-hive-backend.git
git pull origin dev
```

3. **Create feature branch:**

```bash
git checkout -b PH-001/feat/your-feature-name
```

4. **Make changes and commit:**

```bash
git add .
git commit -m "feat: add your feature description"
```

5. **Push and create PR:**

```bash
git pull origin dev  # Check for conflicts
git push -u origin PH-001/feat/your-feature-name
```

6. **Create Pull Request to `dev` branch**

### Commit Standards

| Type       | Description           |
| ---------- | --------------------- |
| `feat`     | New feature           |
| `fix`      | Bug fix               |
| `docs`     | Documentation changes |
| `style`    | Code style changes    |
| `refactor` | Code refactoring      |
| `test`     | Adding/updating tests |
| `chore`    | Maintenance tasks     |

**Sample Commits:**

- `feat: add property image upload functionality`
- `fix: resolve authentication token expiry issue`
- `docs: update API endpoint documentation`

## Testing

Run tests with:

```bash
python manage.py test
```

## License

This project is licensed under the MIT License.

## Support

For support, email: support@propertyhive.com.ng
