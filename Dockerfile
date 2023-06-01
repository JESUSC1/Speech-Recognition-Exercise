# Use a base image with Jupyter and necessary dependencies
FROM jupyter/datascience-notebook:latest

# Switch to root user to install system dependencies
USER root

# Install necessary build dependencies
RUN apt-get update && \
    apt-get install -y autoconf automake libtool libsndfile1-dev

# Switch back to the notebook user
USER $NB_UID

# Copy the PortAudio source code into the Docker image
COPY pa_stable_v190700_20210406.tar /tmp/portaudio.tar

# Extract the PortAudio source code
RUN tar -xf /tmp/portaudio.tar -C /tmp && \
    rm /tmp/portaudio.tar

# Set the working directory to the PortAudio source directory
WORKDIR /tmp/portaudio

# Generate the 'configure' script from 'configure.in'
RUN autoreconf -fiv

# Configure and build PortAudio
RUN ./configure && \
    make && \
    make install

# Copy the Jupyter notebook to the home directory
COPY Speech_Recognition_Exercise.ipynb /home/$NB_USER/

# Set permissions for the notebook
RUN chown $NB_UID:$NB_GID /home/$NB_USER/Speech_Recognition_Exercise.ipynb

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Set the working directory to the home directory
WORKDIR /home/$NB_USER

# Start the Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
