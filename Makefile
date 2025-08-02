# Makefile for Docker management of genai-bot project
# This Makefile contains commands to build, run, and manage the Docker container for the genai-bot project.
# It also includes commands to push the Docker image to AWS ECR.
# Ensure you have Docker and AWS CLI installed and configured before running these commands.

# Clean up Docker system
clean_docker:
	docker system prune -a

# Basic Docker commands
build_image:
	docker build -t genai-bot .

run_container:
	docker run -d --name genai-bot-container -v .:/app -p 8081:8081 genai-bot


###### Push Your Image to ECR

# get login credentials
get_ecr_login:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 474668428902.dkr.ecr.us-east-1.amazonaws.com

# Tag image for ECR:
tag_image:
	docker tag genai-bot 474668428902.dkr.ecr.us-east-1.amazonaws.com/genai-bot-repo

# Push the image to ECR
push_to_ecr:
	docker push 474668428902.dkr.ecr.us-east-1.amazonaws.com/genai-bot-repo

# Add helpful commands for Docker management
stop_container:
	docker stop genai-bot-container

remove_container:
	docker rm genai-bot-container

# Clean up command
clean: stop_container remove_container
	docker rmi genai-bot

# Development commands
dev: build_image run_container

# Restart command
restart: stop_container remove_container run_container

# Show container logs
logs:
	docker logs -f genai-bot-container

# Show container status
status:
	docker ps -a | grep genai-bot

.PHONY: build_image run_container stop_container remove_container clean dev restart logs status