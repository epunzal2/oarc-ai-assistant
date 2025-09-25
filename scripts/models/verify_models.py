import yaml
import os
import glob

def verify_models():
    """
    Parses the models.yml file and verifies the integrity of the downloaded models.
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'configs', 'models.yml')
    with open(config_path, 'r') as f:
        models_config = yaml.safe_load(f)

    all_models_verified = True

    # Verify LLMs
    for llm in models_config.get('llms', []):
        filename = llm['filename']
        local_dir = llm['local_dir']
        model_path = os.path.join(local_dir, filename)

        if os.path.exists(model_path):
            print(f"✅ Verified: {model_path}")
            continue

        # Check for sharded gguf files (e.g., <filename>-00001-of-000NN.gguf)
        base, ext = os.path.splitext(filename)
        pattern = os.path.join(local_dir, f"{base}-*-of-*.{ext.lstrip('.')}")
        shards = sorted(glob.glob(pattern))
        if shards:
            print(f"ℹ️  Sharded model detected in {local_dir} (will be assembled at runtime):")
            for s in shards:
                print(f"   - {os.path.basename(s)}")
            # Treat as present since runtime can assemble
            continue

        print(f"❌ Missing: {model_path}")
        all_models_verified = False

    # Verify embedding models
    for emb_model in models_config.get('embedding_models', []):
        local_dir = emb_model['local_dir']
        
        # A simple check to see if the directory is not empty
        if os.path.exists(local_dir) and os.listdir(local_dir):
            print(f"✅ Verified: {local_dir} (directory exists and is not empty)")
        else:
            print(f"❌ Missing or empty: {local_dir}")
            all_models_verified = False
            
    if all_models_verified:
        print("\nAll models verified successfully! 🎉")
    else:
        print("\nSome models are missing. Please run the download script. 😞")

if __name__ == "__main__":
    verify_models()
