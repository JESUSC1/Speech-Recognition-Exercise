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

# Set the working directory to the root of the repository
WORKDIR /home/$NB_USER/Speech-Recognition-Exercise

# Start the Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]



# Here's a breakdown of the steps in your Dockerfile:

# 1. The base image jupyter/datascience-notebook:latest is used, which already includes Jupyter and #necessary dependencies.
# 2. The user is switched to root to install system dependencies.
# 3. The necessary build dependencies are installed using apt-get.
# 4. The PortAudio source code is copied into the Docker image.
# 5. The PortAudio source code is extracted and the ownership is changed to the notebook user.
# 6. The working directory is set to the PortAudio source directory.
# 7. The 'configure' script is generated from 'configure.in'.
# 8. The user is switched back to root to install the PortAudio library.
# 9. The PortAudio library is configured, built, and installed.
# 10. The user is switched back to the notebook user.
# 11.The notebook file Speech_Recognition_Exercise.ipynb is copied to the user's home directory.
# 12. The Python dependencies listed in requirements.txt are installed using pip.
# 13. The working directory is set to the root of the repository (/home/$NB_USER/Speech-Recognition-Exercise).
# 14. The Jupyter Lab is started with the specified command.

