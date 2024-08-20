# Use the official Python image as a base image
FROM python:3.10-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y \
  gcc \
  python3-dev \
  default-libmysqlclient-dev \
  build-essential \
  pkg-config \
  && apt-get clean

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# COPY entrypoint.sh /app/entrypoint.sh


# Copy the rest of the application code to the working directory
COPY . /app/

# RUN chmod +x /app/entrypoint.sh

# Expose the port
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
