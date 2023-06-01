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

# Switch back to the notebook user
USER $NB_UID

# Set the working directory to the home directory
WORKDIR /home/$NB_USER

# Copy the Jupyter notebook to the home directory
COPY Speech_Recognition_Exercise.ipynb /home/$NB_USER/

# Mount the repository directory as a volume
VOLUME /home/$NB_USER

# Start the Jupyter Notebook
# CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]

# Start the Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
