# Use a base image
FROM jupyter/datascience-notebook

# Copy the PortAudio files to the /usr/local/ directory
COPY dependencies/portaudio/ /usr/local/

# Copy the requirements.txt file to the working directory
COPY src/requirements.txt .

# Install PortAudio system dependency
RUN apt-get update && apt-get install -y portaudio19-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files to the working directory
COPY src/ .

# Set the entry point command (if needed)
# ENTRYPOINT [ "python", "your_script.py" ]
ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

