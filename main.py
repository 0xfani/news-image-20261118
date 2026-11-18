import os
import shutil
from pathlib import Path

# copy the finished front page of 18 November 2026 to the output folder
# (/output in the make.fun sandbox; MAKEFUN_OUTPUT_DIR when testing locally)
out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
out_dir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(Path(__file__).parent / "entry.png", out_dir / "entry.png")
