# Dockerfile
FROM python:3.11.9

# Set the PYTHONPATH to include src/
ENV PYTHONPATH=/app/src

# Copy the application code
WORKDIR /app
COPY src/ /app/src/

# Set working directory

# Expose default http.server port
EXPOSE 8000

WORKDIR /app/src
CMD ["python3", "serve.py"]
