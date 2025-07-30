import sys

try:
    import config
except ImportError as e:
    print(
        "[ERROR] Cannot find config.py. Please copy it from config.py.example",
        file=sys.stderr)
    exit(1)
except Exception as e:
    print("[ERROR] Invalid config.py", file=sys.stderr)
    exit(1)

