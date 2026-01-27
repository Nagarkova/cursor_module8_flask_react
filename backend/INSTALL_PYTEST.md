# Installing pytest and Test Dependencies

## Issue
The error "Package `pytest` is not installed in the selected environment" occurs because pytest needs to be installed in your Python environment.

## Solution

### Option 1: Install in Virtual Environment (Recommended)

1. **Activate your virtual environment:**
   ```bash
   cd backend
   source venv/bin/activate  # On macOS/Linux
   # OR
   venv\Scripts\activate     # On Windows
   ```

2. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Or install just test dependencies:**
   ```bash
   pip install pytest==7.4.3 pytest-flask==1.3.0 pytest-cov==4.1.0
   ```

4. **Verify installation:**
   ```bash
   pytest --version
   ```

### Option 2: Create Virtual Environment (If you don't have one)

1. **Create virtual environment:**
   ```bash
   cd backend
   python3 -m venv venv
   ```

2. **Activate it:**
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Option 3: Use the Installation Script

```bash
cd backend
chmod +x install_test_dependencies.sh
./install_test_dependencies.sh
```

## Verification

After installation, verify pytest is installed:

```bash
python3 -c "import pytest; print(f'pytest {pytest.__version__} installed')"
pytest --version
```

## Note

The `requirements.txt` file is correct and includes:
- pytest==7.4.3
- pytest-flask==1.3.0
- pytest-cov==4.1.0

You just need to install these packages in your active Python environment.
