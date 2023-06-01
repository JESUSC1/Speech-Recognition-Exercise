FROM ubuntu:latest

USER root

# Install necessary build dependencies
RUN apt-get update && \
    apt-get install -y autoconf automake libtool gcc g++

# Copy the PortAudio source code into the Docker image
COPY pa_stable_v190700_20210406.tar /tmp/portaudio.tar

# Extract the PortAudio source code
RUN tar -xf /tmp/portaudio.tar -C /tmp && \
    rm /tmp/portaudio.tar

# Set the working directory to the PortAudio source directory
WORKDIR /tmp/portaudio-2.0.0

# Generate the 'configure' script from 'configure.in'
RUN autoreconf -i

# Configure and build PortAudio
RUN ./configure && \
    make && \
    make install

# Switch back to the default user
USER $NB_UID

# Optionally, you can include additional steps specific to your project, such as installing Python packages or setting up the notebook environment.

# Start the Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]

