from celery import Celery
from rate_limiter import RateLimiter
from flask import Flask, request, jsonify
app = Celery('tasks')
app.config_from_object('celeryconfig')

rate_limiter = RateLimiter(max_calls=5, period=60)  # Example: 5 calls per minute

@app.task
def add(x, y):
    return x + y

@app.task
@rate_limiter.limit
def multiply(x, y):
    return x * y

@app.task
def subtract(x, y):
    return x - y

@app.task
def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y