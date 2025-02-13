1. Go to https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe, download and install
2. In the Install dialog check "Add Python 3.6 to PATH" before click "Install"
3. From https://github.com/andrewgrow/Support click "Clone or download", select "Download zip"
3. Unzip a directory with project and run App.py

# Setup and Run Instructions for macOS

## 🚀 Method 1: Using Docker (Recommended)
This method ensures that the script runs in a controlled environment without compatibility issues.

### 1. Install Docker
- Download and install **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** for macOS.

### 2. Create `Dockerfile` in the Project Directory
Add the following content to a file named `Dockerfile`:

```dockerfile
FROM python:3.5
WORKDIR /app
COPY . .
CMD ["python", "App.py"]
```

### 3. Build and Run the Docker Container
```sh
docker build -t support-app .
docker run --rm -it -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" support-app
```
- The `-v` flag mounts local directories `input` and `output` into the container.
- `--rm` ensures the container is removed after execution.

---

## 🛠 Method 2: Using `pyenv` (Alternative)
If you prefer running the script natively without Docker, use `pyenv` to install and manage Python 3.5.

### 1. Install `pyenv`
```sh
brew install pyenv
```

### 2. Configure `pyenv`
Add the following to `~/.zshrc` (or `~/.bashrc` if using Bash):
```sh
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
```
Then apply the changes:
```sh
source ~/.zshrc  # or source ~/.bashrc
```

### 3. Install Python 3.5 Using `pyenv`
```sh
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.5.10
pyenv global 3.5.10
```

### 4. Create Required Directories
```sh
mkdir -p input output
```

### 5. Run the Script
```sh
python App.py
```

---

## 📂 Folder Structure
Ensure your project directory looks like this before running the script:
```
project-root/
│── App.py
│── Dockerfile (if using Docker)
│── README.md
│── input/       # Place input files here
│── output/      # Processed files will be stored here
```

---

## ✅ Choosing the Best Method
- **Docker (Method 1)** is recommended for consistency across systems.
- **Pyenv (Method 2)** is useful if you want to run Python directly on macOS without a container.

Choose the method that best suits your setup

