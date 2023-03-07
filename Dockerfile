# Use an official Python runtime as the base image
FROM python:3.9-slim

COPY . .

RUN pip install -r requirements.txt

# Copy the rest of the application files into the container
COPY . /financial

WORKDIR /api

# Expose the port on which the application will run
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]