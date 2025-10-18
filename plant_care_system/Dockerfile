# plant_care_system/Dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create static and media directories
RUN mkdir -p /app/staticfiles /app/media

# Set permissions
RUN chown -R www-data:www-data /app
USER www-data

# Run gunicorn
CMD ["gunicorn", "plant_care.wsgi:application", "--bind", "0.0.0.0:8000"]