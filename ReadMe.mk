# Deployment thingy

## Backend
To run the backend server:

1.  Activate the virtual environment:
    ```bash
    env\Scripts\activate
    ```
2.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
3.  Start the Django development server:
    ```bash
    python manage.py runserver
    ```

## Frontend
To run the frontend development server:

// The name lol, next time change the 'mane'
1.  Navigate to the `forntend` directory (Note that is `forntend` instead of `frontend`, i found it kinda funny, typo stays!):
    ```bash
    cd forntend
    ```
// You forgot the 'npm install' command
2.  Start the Vite/Next.js development server:
    ```bash
    npm run dev
    ```

## Test Users

### Admin User
- **Username:** `Admin`
- **Password:** `Admin123`

### Normal User
- **Username:** `1`
- **Password:** `123`
*(Or any that gets created on the register page)*