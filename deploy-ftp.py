import os
import subprocess
import sys

PROXY = "http://127.0.0.1:7897"
FTP_HOST = "212.85.28.149"
FTP_USER = "u868313694.insurancetipspro.com"
FTP_PASS = "Xxh113324~"
REMOTE_BASE = ""
LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

EXCLUDE = {
    'node_modules', '.git', 'deploy-ftp.js', 'deploy-ftp.py',
    'ftp-test.py', 'ftp-test2.py', 'ftp-test3.py', 'ftp-test-path.py',
    'ftp-deploy-out.txt', 'ftp-deploy-err.txt',
    '.gitignore', 'package-lock.json', '__pycache__',
    'ftp-err2.txt', 'ftp-err3.txt', 'ftp-err4.txt',
    'ftp-out2.txt', 'ftp-out3.txt', 'ftp-out4.txt',
}


def curl_upload(local_file, remote_path):
    """Upload a single file via curl through proxy."""
    url = f"ftp://{FTP_HOST}{remote_path}"
    cmd = [
        "curl",
        "--proxytunnel",
        "--proxy", PROXY,
        "--insecure",
        "--silent",
        "--show-error",
        "--ftp-create-dirs",
        "--connect-timeout", "30",
        "--max-time", "240",
        "-u", f"{FTP_USER}:{FTP_PASS}",
        "-T", local_file,
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()}")
        return False
    return True


def collect_files(local_dir, remote_dir, files_list):
    """Recursively collect all files to upload."""
    items = sorted(os.listdir(local_dir))
    for item in items:
        if item in EXCLUDE:
            continue
        local_path = os.path.join(local_dir, item)
        remote_path = remote_dir + '/' + item
        if os.path.isdir(local_path):
            collect_files(local_path, remote_path, files_list)
        else:
            files_list.append((local_path, remote_path))


def main():
    print(f'Deploying from: {LOCAL_DIR}')
    print(f'Target: ftp://{FTP_HOST}{REMOTE_BASE}')
    print()

    files = []
    collect_files(LOCAL_DIR, REMOTE_BASE, files)
    total = len(files)
    print(f'Found {total} files to upload\n')

    success = 0
    failed = []
    for i, (local_path, remote_path) in enumerate(files, 1):
        rel = remote_path.replace(REMOTE_BASE + '/', '')
        print(f'[{i}/{total}] {rel}', end=' ... ', flush=True)
        ok = False
        for attempt in range(3):
            ok = curl_upload(local_path, remote_path)
            if ok:
                break
            if attempt < 2:
                print(f'retry {attempt+2}', end=' ... ', flush=True)
        if ok:
            print('OK')
            success += 1
        else:
            print('FAILED')
            failed.append((local_path, remote_path))

    print(f'\n{"="*50}')
    print(f'Done: {success}/{total} files uploaded successfully')
    if failed:
        print(f'\nFailed files:')
        for _, f in failed:
            print(f'  {f}')
        sys.exit(1)
    else:
        print('All files uploaded!')


if __name__ == '__main__':
    main()
