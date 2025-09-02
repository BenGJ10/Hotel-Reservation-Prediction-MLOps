# Use Jenkins LTS as the base image
FROM jenkins/jenkins:lts

# Switch to root user to install Docker
USER root

# Install Docker (auto-detects arm64/amd64 and Debian version)
RUN apt-get update -y && apt-get install -y curl gnupg lsb-release && \
    curl -fsSL https://get.docker.com | sh && \
    apt-get clean

# Add Jenkins user to the Docker group
RUN groupadd -f docker && usermod -aG docker jenkins

# Create Docker data directory
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Switch back to Jenkins user
USER jenkins
