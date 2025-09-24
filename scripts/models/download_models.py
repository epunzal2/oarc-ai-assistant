import yaml
import subprocess
import os

def download_models():
    """
    Parses the models.yml file and downloads the models using huggingface-cli.
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'configs', 'models.yml')
    with open(config_path, 'r') as f:
        models_config = yaml.safe_load(f)

    # Download LLMs
    for llm in models_config.get('llms', []):
        repo_id = llm['repo_id']
        filename = llm['filename']
        local_dir = llm['local_dir']
        
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
            
        command = [
            "huggingface-cli", "download", repo_id, filename,
            "--local-dir", local_dir,
            "--local-dir-use-symlinks", "False"
        ]
        print(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True)

    # Download embedding models
    for emb_model in models_config.get('embedding_models', []):
        repo_id = emb_model['repo_id']
        local_dir = emb_model['local_dir']
        
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        command = [
            "huggingface-cli", "download", repo_id,
            "--local-dir", local_dir,
            "--exclude", "*.onnx",
            "--local-dir-use-symlinks", "False"
        ]
        print(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True)

if __name__ == "__main__":
    download_models()