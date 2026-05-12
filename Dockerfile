FROM python:3.12-slim

# Create a non-root user and group to run the application
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -u 1000 appuser

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/app.py .

# Create writable directories and set permissions for the application directory and a temporary directory
RUN mkdir -p /tmp/app && \
    chown -R appuser:appgroup /app /tmp/app

USER appuser

EXPOSE 5555

CMD ["python", "app.py"]