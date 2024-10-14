FROM python:3.10.5
# RUN pip install --root-user-action=ignore 
ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m pip install --upgrade pip && apt-get update \
&& apt-get update && apt-get install -y libgdal-dev && apt-get install -y gdal-bin python3-gdal \
&& apt-get install libpq-dev -y && apt-get install gdal-bin && apt-get install nginx \
&& pip install -r requirements.txt
# RUN add-apt-repository ppa:ubuntugis/ppa && apt-get update && apt-get install -y gdal-bin python-gdal python3-gdal

# RUN python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# ENV PIP_ROOT_USER_ACTION=ignore
# pip install libgdal-dev
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
EXPOSE 8000

# RUN python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# # Use the official Miniconda image as the base image
# FROM continuumio/miniconda3

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONBUFFERED 1

# # Create and set the working directory
# WORKDIR /bulletin
# # Install mamba for faster package management and create a new environment
# RUN conda install -y mamba -n base -c conda-forge \
#     && mamba create -n myenv python=3.12.0 -y \
#     && conda run -n myenv mamba install -c conda-forge gdal libgdal gcc fiona wordcloud \
#     && conda clean -afy

# # Activate the environment
# SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# # Copy the requirements file into the container
# COPY requirements.txt .

# # Install pip in the conda environment
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of your application code into the container
# COPY . .

# # Expose the port that the application will listen on
# EXPOSE 8000

# # Start the Web UI
# CMD ["conda", "run", "-n", "myenv", "lida", "ui", "--host", "0.0.0.0", "--port", "8000", "--docs"]


