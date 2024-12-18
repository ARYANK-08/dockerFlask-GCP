# Use a slim Python image as a base
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /todo-app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies in the container
RUN pip3 install -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose port 8080
EXPOSE 8080

# Command to run the application
CMD ["python", "app.py"]
