# Use the official Python image as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app
RUN pip install --upgrade pip
RUN apt-get update

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get install -y unixodbc-dev
# Copy the rest of the files to the container 
COPY . .

# Expose the port that streamlit uses
EXPOSE 8501

ENV PORT=8501

# Define the command to run the streamlit app
CMD streamlit run app.py --server.port $PORT

