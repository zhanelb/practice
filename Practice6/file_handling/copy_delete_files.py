import shutil
import os
shutil.copy("sample.txt", "backup.txt")
if os.path.exists("backup.txt"):
    print("Backup exists")
os.remove("backup.txt")
print("Backup deleted")