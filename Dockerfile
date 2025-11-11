# Use official Apify base image for Python
FROM apify/actor-python:3.11

# Copy all files to /usr/src/app (Apify's working directory)
COPY . ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the actor
CMD ["python", "main.py"]
