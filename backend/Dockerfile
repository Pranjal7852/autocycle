# Use a Conda base image
FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Copy environment.yml to define dependencies
COPY environment.yml .

# Create Conda environment from environment.yml
RUN conda env create -f environment.yml && \
    conda clean --all --yes

# Ensure the env name matches your environment.yml
ARG ENV_NAME=dps-ai-pipeline
ENV PATH /opt/conda/envs/$ENV_NAME/bin:$PATH

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Create logs directory
RUN mkdir -p /app/logs

# Expose FastAPI port
EXPOSE 8000

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Start app with uvicorn (recommended for FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]