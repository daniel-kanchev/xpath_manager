import dropbox
import login_data
import config
import os


def download_db():
    dbx = dropbox.Dropbox(login_data.dropbox_access_token)
    print("Downloading database..")
    dbx.files_download_to_file(path=f'/{config.db_path}', download_path=f'./{config.db_path}')
    while not os.path.exists(config.db_path):
        time.sleep(1)
    print("Download finished.")


def upload_db():
    dbx = dropbox.Dropbox(login_data.dropbox_access_token)
    print("Uploading database..")
    with open('log.db', 'rb') as f:
        dbx.files_upload(f.read(), '/log.db', mode=dropbox.files.WriteMode.overwrite)
    print("Upload finished.")


if __name__ == "__main__":
    choice = 0
    while choice != 'u' and choice != 'd':
        choice = input("Do you wish to upload or download the database?(upload - u, download - d)\n:")

    if choice == 'u':
        upload_db()
    else:
        download_db()
