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
    chown -R $NB_UID:$NB_GID /tmp/portaudio

# Set the working directory to the PortAudio source directory
WORKDIR /tmp/portaudio

# Generate the 'configure' script from 'configure.in'
RUN autoreconf -fiv

# Switch to root user
USER root

# Install the PortAudio library
RUN ./configure && \
    make && \
    make install

# Switch back to non-root user
USER $NB_UID

# Copy the notebook file to the user's home directory
COPY Speech_Recognition_Exercise.ipynb /home/$NB_USER/

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Set the permissions for the notebook file
RUN chown $NB_UID:$NB_GID /home/$NB_USER/Speech_Recognition_Exercise.ipynb \
    && chmod 664 /home/$NB_USER/Speech_Recognition_Exercise.ipynb

# By using chmod 664, the notebook file will be readable and writable by the user running the Jupyter Notebook 
# server inside the container, as well as by members of the same group. Other users will have read-only access to the file

# By using chmod 644, the notebook file will be readable by the user running the Jupyter Notebook 
# server inside the container, as well as by members of the same group. Other users will have read-only access to the file

# Set the working directory to the home directory
WORKDIR /home/$NB_USER

# Start the Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
