import os
import shutil
import subprocess
import sys
import platform

# Step 1: Create a virtual environment in the workspace folder
workspace_dir = os.getcwd()  # Current working directory for workspace
venv_path = os.path.join(workspace_dir, '.venv')

try:
    # Check if the .venv folder exists; if so, delete it
    if os.path.exists(venv_path):
        print(f"Virtual environment folder already exists at {venv_path}. Deleting it...")
        shutil.rmtree(venv_path)

    print(f"Creating virtual environment at {venv_path}...")
    subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)

    # Ensure the virtual environment is activated in Python subprocesses
    venv_python = os.path.join(venv_path, 'Scripts', 'python') if platform.system() == 'Windows' else os.path.join(venv_path, 'bin', 'python')
    venv_pip = os.path.join(venv_path, 'Scripts', 'pip') if platform.system() == 'Windows' else os.path.join(venv_path, 'bin', 'pip')

    # Step 2: Install pip and upgrade it
    print("Upgrading pip in the virtual environment...")
    subprocess.run([venv_pip, 'install', '--upgrade', 'pip'], check=True)

    # Step 3: Install python-dotenv inside the virtual environment
    print("Installing python-dotenv in the virtual environment...")
    subprocess.run([venv_pip, 'install', 'python-dotenv'], check=True)

    # Step 4: Load environment variables from .env file using python-dotenv
    from dotenv import load_dotenv
    load_dotenv()

    # Get sensitive information from the environment
    # https://colab.research.google.com/drive/19AJ2q_43-9IRBG1fT0ztULh12OUtjL_l
    github_token = os.getenv('GITHUB_TOKEN')  # Load GitHub token from .env
    user_name = os.getenv('GITHUB_USERNAME')  # Load GitHub username from .env
    repo_name = 'pc-gym'  # Replace with your repository name

    # Check if token and username are loaded
    if not github_token or not user_name:
        raise ValueError("GitHub token or username is missing. Please check your .env file.")

    # Format the URL with the token for cloning
    repo_url = f'https://{github_token}@github.com/{user_name}/{repo_name}.git'

    # Step 5: Install other necessary packages
    print("Installing pcgym...")
    subprocess.run([venv_pip, 'install', 'pcgym'], check=True)
    print("Installing optuna...")
    subprocess.run([venv_pip, 'install', 'optuna'], check=True)
    print("Installing stable-baselines3...")
    subprocess.run([venv_pip, 'install', 'stable-baselines3'], check=True)
    print("Installing Jupyter and ipywidgets")
    subprocess.run([venv_pip, 'install', 'jupyter', 'ipywidgets'], check=True)

    # Step 6: Clone the repository
    print(f"Cloning repository: {repo_url}")
    subprocess.run(['git', 'clone', repo_url], check=True)

    # Step 7: Navigate into the cloned repository directory
    repo_dir = os.path.join(workspace_dir, repo_name)
    os.chdir(repo_dir)
    print(f"Changed directory to {repo_dir}")

    # Step 8: Install requirements from the repository's requirements.txt
    repo_requirements = os.path.join(repo_dir, 'requirements.txt')
    if os.path.exists(repo_requirements):
        print(f"Installing requirements from {repo_requirements}...")
        subprocess.run([venv_pip, 'install', '-r', repo_requirements, '--quiet'], check=True)
    else:
        print(f"No requirements.txt found in the repository directory.")

    print("Setup completed successfully.")
except subprocess.CalledProcessError as e:
    print(f"An error occurred while executing a command: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
