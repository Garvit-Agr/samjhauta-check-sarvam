import sys
from pathlib import Path

# Ensure root workspace directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import os
import uvicorn
from samjhautacheck.config import HOST, PORT


def main():
    host = os.getenv("HOST", HOST)
    port = int(os.getenv("PORT", str(PORT)))
    print(f"Starting SamjhautaCheck server on http://{host}:{port}")
    uvicorn.run("samjhautacheck.app:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
