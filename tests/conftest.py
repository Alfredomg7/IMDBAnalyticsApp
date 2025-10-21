import sys
from pathlib import Path

# Add the App directory to Python path so we can import modules
app_dir = Path(__file__).parent.parent
sys.path.insert(0, str(app_dir))
