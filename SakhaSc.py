import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

folder_id = '1Sj_Rnuipoi9i90i9009890aI22R8y8y8y3a7k5Ncas'
destination_path = '/home/test-user/'

if not os.path.isdir(destination_path):
    print("Указанный путь к серверу не существует.")
    exit()

folder = drive.CreateFile({'id': folder_id})
folder.GetContentFile(os.devnull)

if not os.path.exists(os.devnull):
    print("Нет доступа к папке Sakha на Google Drive.")
    exit()

file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
success = False

for file in file_list:
    if file['mimeType'] == 'application/vnd.google-apps.folder':
        folder_path = os.path.join(destination_path, file['title'])
        os.makedirs(folder_path)
        subfile_list = drive.ListFile({'q': f"'{file['id']}' in parents and trashed=false"}).GetList()
        for subfile in subfile_list:
            if subfile['title'].endswith(('.gif', '.tiff', '.geotiff', '.kml', '.mp4')):
                download_path = os.path.join(folder_path, subfile['title'])
                subfile.GetContentFile(download_path)
                success = True   
    elif file['title'].endswith(('.gif', '.tiff', '.geotiff', '.kml', '.mp4')):
        download_path = os.path.join(destination_path, file['title'])
        file.GetContentFile(download_path)
        success = True

if success:
    print("Файлы успешно загружены на сервер")
else:
    print("Нет файлов для загрузки")

