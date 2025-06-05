import sys
import subprocess

if len(sys.argv) < 2:
    sys.exit("No URL provided")

url = sys.argv[1].strip()

subprocess.run(["open", url])
