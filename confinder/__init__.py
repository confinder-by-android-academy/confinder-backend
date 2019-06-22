from pathlib import Path

BASE = Path(__file__).parent
configs = (
    BASE / 'config.yaml',
    *list(BASE.glob('*/config.yaml')),
)
