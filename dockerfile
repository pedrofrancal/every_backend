# Use the official Python image as the base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Load environment variables from the .env file and run the app using Gunicorn
CMD ["gunicorn", "-w", "4", "-k", "gthread", "-b", "0.0.0.0:8000", "wsgi:app"]
