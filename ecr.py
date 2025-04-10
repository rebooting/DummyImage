import boto3
import subprocess
import base64
import os

# Configuration
region = os.getenv("AWS_REGION", "us-east-1")  # Automatically obtain region from environment variable, default to 'us-east-1'
repository_name = "dummy-image"  # Replace with your ECR repository name
image_tag = "latest"  # Replace with your desired image tag

# Step 1: Authenticate with ECR
ecr_client = boto3.client("ecr", region_name=region)

def create_ecr():
    # Step 1: Authenticate with ECR
    auth_token = ecr_client.get_authorization_token()
    username, password = base64.b64decode(auth_token["authorizationData"][0]["authorizationToken"]).decode().split(":")
    registry_url = auth_token["authorizationData"][0]["proxyEndpoint"]

    # Log in to Docker
    subprocess.run(["docker", "login", "-u", username, "-p", password, registry_url], check=True)

    # Step 2: Build and Tag the Docker Image
    image_name = f"{registry_url.replace('https://', '')}/{repository_name}:{image_tag}"
    subprocess.run(["docker", "build", "-t", image_name, "."], check=True)

    # Step 3: Push the Image to ECR
    subprocess.run(["docker", "push", image_name], check=True)

    print(f"Image successfully pushed to {image_name}")

    # Step 4: Tag the ECR Repository
    tags = [
        {"Key": "Environment", "Value": "Dev"},
        {"Key": "Project", "Value": "DummyImage"}
    ]

    ecr_client.tag_resource(
        resourceArn=ecr_client.describe_repositories(repositoryNames=[repository_name])["repositories"][0]["repositoryArn"],
        tags=tags
    )

    print(f"Tags successfully added to the ECR repository: {repository_name}")

def destroy_ecr():
    try:
        # Step 1: Delete all images in the repository
        images = ecr_client.list_images(repositoryName=repository_name)["imageIds"]
        if images:
            ecr_client.batch_delete_image(repositoryName=repository_name, imageIds=images)
            print(f"All images in the repository '{repository_name}' have been deleted.")
        else:
            print(f"No images found in the repository '{repository_name}'.")

        # Step 2: Delete the repository
        ecr_client.delete_repository(repositoryName=repository_name, force=True)
        print(f"ECR repository '{repository_name}' has been deleted successfully.")
    except ecr_client.exceptions.RepositoryNotFoundException:
        print(f"ECR repository '{repository_name}' does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting the ECR repository: {e}")

# Call the function
# create_ecr()

# Call the destroy function
# destroy_ecr()