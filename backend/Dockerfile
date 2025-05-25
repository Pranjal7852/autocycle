# Use a Conda base image
FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Copy environment.yml to define dependencies
COPY environment.yml .

# Create Conda environment from environment.yml
RUN conda env create -f environment.yml && \
    conda clean --all --yes

# Activate the Conda environment by default
# Modify the shell to source Conda
SHELL ["/bin/bash", "--login", "-c"]

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Create logs directory with correct permissions
RUN mkdir -p /app/logs && chown -R appuser:appuser /app/logs

# Expose port (based on your original Dockerfile)
EXPOSE 8000

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run the application using Conda environment
CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "run.py"]