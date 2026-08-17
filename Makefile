.PHONY: setup db-up db-down run clean

# Installs Python dependencies
setup:
	pip install -r requirements.txt

# Starts the database with Docker in the background (detached)
db-up:
	docker-compose -f docker/docker-compose.yml up -d
	@echo "Waiting for SQL Server to start... (wait about 15 seconds before running the pipeline)"

# Stops and removes the database containers
db-down:
	docker-compose -f docker/docker-compose.yml down

# Runs the ETL pipeline
run:
	python src/data_pipeline.py

# Cleans up temporary Python files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
