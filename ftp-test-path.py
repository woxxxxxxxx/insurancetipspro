"""Quick test: upload test.txt to FTP root / and to /public_html/ to find correct document root."""
import subprocess, tempfile, os

PROXY = "http://127.0.0.1:7897"
FTP_HOST = "212.85.28.149"
FTP_USER = "u868313694.insurancetipspro.com"
FTP_PASS = "Xxh113324~"

def upload(remote_path, content):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(content)
        tmp = f.name
    url = f"ftp://{FTP_HOST}{remote_path}"
    cmd = ["curl", "--proxytunnel", "--proxy", PROXY, "--insecure",
           "--silent", "--show-error", "--ftp-create-dirs",
           "-u", f"{FTP_USER}:{FTP_PASS}", "-T", tmp, url]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    os.unlink(tmp)
    if result.returncode == 0:
        print(f"  Uploaded OK → {remote_path}")
    else:
        print(f"  FAILED {remote_path}: {result.stderr.strip()}")

# Try FTP root, /public_html, and common Hostinger addon-domain paths
upload("/ftp-probe-root.txt",        "root-level")
upload("/public_html/ftp-probe-pub.txt", "public_html-level")
upload("/domains/insurancetipspro.com/public_html/ftp-probe-domain.txt", "domains-path")

print("\nNow test via HTTP which one is accessible:")
print("  curl https://insurancetipspro.com/ftp-probe-root.txt")
print("  curl https://insurancetipspro.com/ftp-probe-pub.txt")
print("  curl https://insurancetipspro.com/ftp-probe-domain.txt")
