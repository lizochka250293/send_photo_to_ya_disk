from datetime import datetime

from yadisk import YaDisk, exceptions


def get_file_info(bot, message):
    file_info = None
    if message.content_type == "document":
        file_info = bot.get_file(message.document.file_id)
    elif message.content_type == 'photo':
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    elif message.content_type == "text":
        return False
    return file_info


class DiskConnector:
    token = None
    disk = None

    def __init__(self):
        pass

    def set_token(self, token):
        self.token = token
        self.disk = YaDisk(token=self.token)

    def check_token(self):
        return self.disk.check_token()

    def upload(self, bot, message):
        date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
        file_info = get_file_info(bot, message)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'files/' + file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            path = new_file.name.split("/")
            file_to_path = "{}.{}".format(date, path[2])
        if self.check_token():
            try:
                self.disk.mkdir("/telegram")
            except exceptions.DirectoryExistsError:
                pass
            print('Directory created!')

            self.disk.upload(f"{src}", f"/telegram/{file_to_path}")
            return True
        return False
