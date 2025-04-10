# Use the official Debian base image
FROM debian:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the runner script and index.html into the container
COPY runner /app/runner
COPY index.html /app/index.html

# Make the runner script executable
RUN chmod +x /app/runner

# Expose port 7010
EXPOSE 7010

# Use the runner script as the entry point
CMD ["/app/runner"]