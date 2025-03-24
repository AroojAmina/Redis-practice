
# Celery and Redis Practice Project

This project is designed to help you practice using Celery with Redis as a message broker and result backend in a Flask application. It includes a simple API that allows you to trigger background tasks and check their status.

## Setup Instructions

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Redis**
   You can start Redis using Docker with the provided `docker-compose.yml` file:
   ```bash
   docker-compose up -d
   ```

5. **Run the Flask Application**
   ```bash
   python -m app.app
   ```

6. **Run Celery Worker**
   In a new terminal, activate the virtual environment and run:
   ```bash
   celery -A app.tasks worker --loglevel=info
   ```

## Usage

- **Trigger a Background Task**
  Send a GET request to `/run-task/<num>` where `<num>` is the number of seconds the task should sleep.

- **Check Task Status**
  Send a GET request to `/task-status/<task_id>` to check the status of a task.

## Testing

To run the tests, ensure your virtual environment is activated and run:
```bash
pytest
```

