#!/bin/bash

# Install test dependencies script
# This script installs pytest and related testing packages

echo "Installing test dependencies..."

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Virtual environment not activated"
    echo "Please activate your virtual environment first:"
    echo "  source venv/bin/activate"
    exit 1
fi

# Install pytest and related packages
pip install pytest==7.4.3
pip install pytest-flask==1.3.0
pip install pytest-cov==4.1.0

# Verify installation
echo ""
echo "Verifying installation..."
python3 -c "import pytest; print(f'✅ pytest {pytest.__version__} installed')" 2>/dev/null || echo "❌ pytest not installed"
python3 -c "import pytest_flask; print('✅ pytest-flask installed')" 2>/dev/null || echo "❌ pytest-flask not installed"
python3 -c "import pytest_cov; print('✅ pytest-cov installed')" 2>/dev/null || echo "❌ pytest-cov not installed"

echo ""
echo "✅ Test dependencies installation complete!"
echo ""
echo "To verify, run: pytest --version"
