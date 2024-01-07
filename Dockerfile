# Use an official Python runtime as a base image
FROM python:3.8


# Set the working directory in the container
WORKDIR /app


# Install any needed packages specified in requirements.txt
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# Copy the app directory contents into the container at /app
COPY ./app /app


# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1337"]
