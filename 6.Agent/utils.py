import os
import re

def parse_code_blocks(response: str):
    """Extract (filename, content) pairs from GPT markdown blocks."""
    pattern = r"```(?:\w+)? filename=(.*?)\n(.*?)```"
    return re.findall(pattern, response, re.DOTALL)

def save_files(code_blocks, root_dir="generated-react-app"):
    for filepath, content in code_blocks:
        full_path = os.path.join(root_dir, filepath.strip())
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ Saved: {full_path}")
    print(f"\n🚀 All files saved in: {root_dir}")

def setup_and_run_app(app_dir="generated-react-app"):
    """Install dependencies and start the React app."""
    import subprocess
    import time
    
    print("\n📦 Installing dependencies...")
    try:
        # Run npm install and wait for it to complete
        subprocess.run(["npm", "install"], cwd=app_dir, check=True)
        print("✅ Dependencies installed successfully")
        
        print("\n🚀 Starting the development server...")
        subprocess.run(["npm", "start"], cwd=app_dir, check=True)
        
        print("\n🌐 Your app should be running at http://localhost:3000")
        print("Press Ctrl+C to stop the server when you're done.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please make sure Node.js is properly installed and you're in the correct directory.")
        raise
    except KeyboardInterrupt:
        print("\n🛑 Shutting down the server...")