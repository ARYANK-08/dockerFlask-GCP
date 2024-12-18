FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /todo-app

# Copy requirements first for caching
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip3 install -r requirements.txt

# Copy all files into the working directory
COPY . .

# Command to run the application
CMD ["python", "app.py"]
