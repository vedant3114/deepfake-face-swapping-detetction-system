import os
import zipfile
import shutil
import urllib.request
import sys

def download_ffmpeg():
    print("Downloading ffmpeg for Windows...")
    # Using a reliable build source (gyan.dev)
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = "ffmpeg_download.zip"
    
    try:
        # Download with progress hook
        def progress(count, block_size, total_size):
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write(f"\rDownloading: {percent}%")
            sys.stdout.flush()
            
        urllib.request.urlretrieve(url, zip_path, reporthook=progress)
        print("\nDownload complete.")
        
        print("Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # List files to find where ffmpeg.exe is
            for file in zip_ref.namelist():
                if file.endswith("bin/ffmpeg.exe"):
                    print(f"Found executable: {file}")
                    # Extract just this file
                    zip_ref.extract(file, ".")
                    # Move to current dir
                    source = file
                    shutil.move(source, "ffmpeg.exe")
                    print("Moved ffmpeg.exe to current directory.")
                    break
                    
        # Cleanup
        print("Cleaning up...")
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        # Clean up the extracted folder structure if needed
        # (The zip usually has a root folder like 'ffmpeg-6.0-essentials_build')
        base_folder = file.split('/')[0]
        if os.path.exists(base_folder) and os.path.isdir(base_folder):
            shutil.rmtree(base_folder)
            
        print("✓ ffmpeg setup successful. Local ffmpeg.exe is ready.")
        
    except Exception as e:
        print(f"\n❌ Error setting up ffmpeg: {e}")

if __name__ == "__main__":
    if os.path.exists("ffmpeg.exe"):
        print("ffmpeg.exe already exists locally.")
    else:
        download_ffmpeg()
