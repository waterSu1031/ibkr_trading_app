from pathlib import Path
from fastapi.templating import Jinja2Templates

# BASE_DIR = Path(__file__).resolve().parent.parent
# template = Jinja2Templates(directory=str(BASE_DIR/"/src/template"))

BASE_DIR = Path(__file__).resolve().parent.parent  # src/
template = Jinja2Templates(directory=str(BASE_DIR / "template"))

# template = Jinja2Templates(directory="src/template")
