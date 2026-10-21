Run import io
import urllib.request
import zipfile

URL = "https://www.ssa.gov/oact/babynames/names.zip"
OUTPUT_CSV = "ssa-baby-names.csv"

# Use browser-like headers so the SSA server does not block the request
req = urllib.request.Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    },
)

with urllib.request.urlopen(req) as response:
    zip_bytes = io.BytesIO(response.read())

with zipfile.ZipFile(zip_bytes) as zf, open(OUTPUT_CSV, "w", encoding="utf-8") as out:
    out.write("year,name,sex,count\n")
    for filename in sorted(zf.namelist()):
        if filename.startswith("yob") and filename.endswith(".txt"):
            year = filename[3:7]
            text = zf.read(filename).decode("utf-8")
            for line in text.splitlines():
                if line.strip():
                    out.write(f"{year},{line.strip()}\n")
