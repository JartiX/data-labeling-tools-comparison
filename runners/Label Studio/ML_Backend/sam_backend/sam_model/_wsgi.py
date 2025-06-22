import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sam_backend.sam_model import SAMModel

def get_ml_model():
    return SAMModel()   