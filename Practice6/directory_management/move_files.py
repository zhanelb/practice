import shutil
shutil.copy("sample.txt", "test_folder/sample_copy.txt")
shutil.move("test_folder/sample_copy.txt", "test_folder/subfolder/sample.txt")
print("Done")