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
WORKDIR /tmp/portaudio-2.0.0

# Generate the 'configure' script from 'configure.in' and build PortAudio
RUN autoconf && ./configure && \
    make && \
    make install

# Switch back to the notebook user
USER $NB_UID

# Copy the Jupyter notebook to the home directory
COPY Speech_Recognition_Exercise.ipynb /home/$NB_USER/

# Start the Jupyter Notebook with the specified notebook file
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.default_url=/home/jovyan/Speech_Recognition_Exercise.ipynb"]
