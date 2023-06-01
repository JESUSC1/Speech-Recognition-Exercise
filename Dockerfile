FROM jupyter/datascience-notebook:latest

USER root

# Copy the tar file to the root directory
COPY pa_stable_v190700_20210406.tar /pa_stable_v190700_20210406.tar

# Extract the contents of the tar file
RUN tar -xf /pa_stable_v190700_20210406.tar

# Install PortAudio from the extracted files
WORKDIR /pa_stable_v190700_20210406
RUN ./configure && make && make install

USER ${NB_USER}

# Copy your project files to the Docker image
COPY --chown=1000:1000 src/ ${HOME}/

# Install Python dependencies
RUN ${KERNEL_PYTHON_PREFIX}/bin/pip install --no-cache-dir -r "${HOME}/requirements.txt"

