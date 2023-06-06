FROM jupyter/datascience-notebook:latest

USER root

# Copy the PortAudio source code into the Docker image
COPY pa_stable_v190700_20210406.tar /tmp/portaudio.tar

# Install necessary build dependencies
RUN apt-get update && \
    apt-get install -y autoconf automake libtool libsndfile1-dev

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

# Install PortAudio system-wide
RUN ldconfig

# Switch back to the notebook user
USER $NB_UID

# Set the working directory to the home directory
WORKDIR /home/$NB_USER

# Copy all files from the root directory to the home directory
COPY . /home/$NB_USER/

# Copy the requirements.txt file to the home directory
COPY requirements.txt /home/$NB_USER/

# Install the dependencies listed in the requirements.txt file
RUN pip install -r requirements.txt

# Set the ALLOW_SAVE environment variable to True
ENV ALLOW_SAVE True

# Mount the repository directory as a volume
VOLUME /home/$NB_USER

# Start the Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]


# Here's a breakdown of the steps in the Dockerfile:

# 1. FROM jupyter/datascience-notebook:latest: This specifies the base image to use for building the Docker image, in this case, the Jupyter datascience-notebook image.
# 2. USER root: Switches to the root user to perform some system-level operations.
# 3. COPY pa_stable_v190700_20210406.tar /tmp/portaudio.tar: Copies the PortAudio source code tarball into the Docker image.
# 4. RUN apt-get update && apt-get install -y autoconf automake libtool libsndfile1-dev: Updates the package lists and installs necessary build dependencies for PortAudio.
# 5. RUN tar -xf /tmp/portaudio.tar -C /tmp && rm /tmp/portaudio.tar: Extracts the PortAudio source code from the tarball into the /tmp/portaudio directory.
# 6. WORKDIR /tmp/portaudio: Sets the working directory to the PortAudio source directory.
# 7. RUN autoreconf -fiv: Generates the 'configure' script from 'configure.in' using autoreconf.
# 8. RUN ./configure && make && make install: Configures, compiles, and installs PortAudio.
# 9. RUN ldconfig: Updates the dynamic linker cache, ensuring that the PortAudio library is properly accessible system-wide.
# 10. USER $NB_UID: Switches back to the default notebook user.
# 11. WORKDIR /home/$NB_USER: Sets the working directory to the home directory of the notebook user.
# 12. COPY . /home/$NB_USER/: Copies all files from the root directory into the home directory.
# 13. COPY requirements.txt /home/$NB_USER/: Copies the requirements.txt file into the home directory.
# 14. RUN pip install -r requirements.txt: Installs the Python dependencies listed in the requirements.txt file.
# 15. ENV ALLOW_SAVE True: Sets the ALLOW_SAVE environment variable to True, allowing changes to be saved in the notebook.
# 16. VOLUME /home/$NB_USER: Mounts the repository directory as a volume, allowing data persistence.
# 17. CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]: Specifies the command to run when the container starts, which is to start Jupyter Lab with appropriate settings.

