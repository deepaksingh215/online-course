# online-course
# Django REST Framework (DRF) Course Enrollment System

This repository contains a Django REST Framework (DRF) application for a course enrollment system. It allows users to browse courses, enroll in courses, and access their enrolled courses.

## Features

- User registration and authentication using JWT tokens.
- Course listing and details API endpoints.
- Enroll in courses and view enrolled courses API endpoints.
- Payment integration with Razorpay for course enrollment.
- Video content management for courses.
- API endpoints for course videos and lecture navigation.

## Installation

1. Clone the repository:
2. Install the required dependencies:
3. Set up the database:
4. Create a superuser:
5. Start the development server:
## API Endpoints

The following API endpoints are available:

- **Registration**: `/api/register/` (POST)
- **Login**: `/api/login/` (POST)
- **Get JWT Token**: `/api/get-token/` (POST)
- **Courses Listing**: `/api/courses/` (GET)
- **Course Details**: `/api/courses/<slug>/` (GET)
- **Enroll in Course**: `/api/courses/<slug>/enroll/` (GET)
- **Enrolled Courses**: `/api/my-courses/` (GET)
- **Create Razorpay Order**: `/api/courses/<slug>/buy-now/` (GET)
- **Verify Payment**: `/api/verify-payment/` (POST)
- **Course Page**: `/api/courses/<slug>/page/` (GET)

## Technologies Used

- Django
- Django REST Framework
- SQlLit3
- Django Knox (JWT authentication)
- Razorpay (Payment integration)

## Contributions

Contributions to this project are welcome. Feel free to open issues or submit pull requests to suggest improvements or add new features.


