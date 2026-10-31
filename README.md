# SOA Reusable Shared Notification Service

A beginner-friendly demo showing how two independent applications reuse one centrally hosted REST API service.

## What it demonstrates
- `canteen_app`: calls the shared service when a food order is placed.
- `student_app`: calls the same shared service when a student update is made.
- `shared_service`: owns the notification business logic and template.
- Change the shared service's template once and both apps receive the updated format on their next API request.

> Important: This updates the functionality returned by the service. It does not automatically rewrite the source code of the two client apps.

## Requirements
- Python 3.10+ (Python 3.11 recommended)
- VS Code
- Internet is not required after Python and dependencies are installed.

## Run in VS Code (Windows)
1. Extract this ZIP file.
2. Open the extracted `soa_reusable_shared_service` folder in VS Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment:
   ```powershell
   py -m venv .venv
   ```
5. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt terminal and run:
   ```bat
   .venv\Scripts\activate.bat
   ```
6. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
7. Start the shared service in Terminal 1:
   ```powershell
   python shared_service/app.py
   ```
   Keep this terminal open. The service runs at `http://127.0.0.1:5000`.
8. Open a second terminal and start the canteen client:
   ```powershell
   python canteen_app/app.py
   ```
   Open `http://127.0.0.1:5001`.
9. Open a third terminal and start the student client:
   ```powershell
   python student_app/app.py
   ```
   Open `http://127.0.0.1:5002`.

## Demonstrate centralized updates
1. Open the shared service dashboard at `http://127.0.0.1:5000`.
2. In the shared service folder, open `shared_service/templates.py`.
3. Change the `MESSAGE_SUFFIX` value, for example from `"Thank you for using our application."` to `"Updated by the central SOA service!"`.
4. Save the file.
5. Stop the shared service with Ctrl+C and start it again with `python shared_service/app.py`.
6. Submit a test notification from both client pages. Both will show the updated message without changing either client app.

The clients fetch the shared template from the API for each request, so the central change is visible on the next request.

## API endpoints
- `GET /health` — service health check
- `GET /api/v1/template` — current shared template/config
- `POST /api/v1/notifications` — create notification
- `GET /api/v1/notifications` — list notifications (demo in-memory storage)
- `GET /` — service dashboard

## Project structure
```text
soa_reusable_shared_service/
├── shared_service/
│   ├── app.py
│   └── templates.py
├── canteen_app/
│   ├── app.py
│   └── templates/index.html
├── student_app/
│   ├── app.py
│   └── templates/index.html
├── requirements.txt
└── README.md
```

## Troubleshooting
- `Address already in use`: stop the previous process or change the port in that app's `app.py`.
- `Connection refused`: start the shared service first and keep it running.
- `ModuleNotFoundError: flask`: activate `.venv` and run `python -m pip install -r requirements.txt`.
- If `py` is not recognized, try `python -m venv .venv`.
- This is an educational local demo. It uses in-memory storage and has no authentication; do not expose it publicly without adding security and persistent storage.
