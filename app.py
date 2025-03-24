from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from celery import Celery
import redis
import time

app = Flask(__name__)


redis_client = redis.Redis(host='localhost', port=6379, db=0)


limiter = Limiter(
    key_func=get_remote_address,  
    storage_uri="redis://localhost:6379",
    app=app
)

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache = Cache(app)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/limited')
@limiter.limit("5 per minute")  
def limited_route():
    return jsonify({"message": "This is a rate-limited route"})

@app.route('/cached')
@cache.cached(timeout=60)  
def cached_route():
    return jsonify({"message": "This is a cached response"})


@celery.task
def long_task(n):
    time.sleep(n) 
    return f"Task completed in {n} seconds"

@app.route('/start_task', methods=['POST'])
def start_task():
    try:
        data = request.get_json()
        if not data or 'duration' not in data:
            return jsonify({"error": "Invalid payload"}), 400
        duration = data.get('duration', 5)  
        task = long_task.delay(duration)
        return jsonify({"task_id": task.id, "status": "Task started"})
    except Exception as e:
        app.logger.error(f"Error starting task: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/task_status/<task_id>')
def task_status(task_id):
    try:
        task = long_task.AsyncResult(task_id)
        if task.state == 'PENDING':
            return jsonify({"status": "Pending"})
        elif task.state == 'SUCCESS':
            return jsonify({"status": "Completed", "result": task.result})
        return jsonify({"status": "In Progress"})
    except Exception as e:
        app.logger.error(f"Error fetching task status: {e}")
        return jsonify({"error": "Invalid task ID"}), 400

@app.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "API is working"})

if __name__ == "__main__":
    app.run(debug=True)
