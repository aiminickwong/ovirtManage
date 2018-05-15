# -*- coding:utf-8 -*-

import os

class upload_receipts_file():
    def __init__(self, name, type=None, size=None,upload_date=None, not_allowed_msg=''):
        self.name = name
        self.type = type
        self.size = size
        self.upload_date = upload_date
        self.not_allowed_msg = not_allowed_msg
        self.url = "/home/xuan/Erp/app/static/data/receipts/%s" % name
        #self.thumbnail_url = "thumbnail/%s" % name  获取每张缩略图
        self.thumbnail_url = "receipts/thumbnail/Picture_icon.png" 
        self.iconurl = "receipts/thumbnail/PDF_ICON.png"
        self.delete_url = "delete/%s" % name
        self.delete_type = "DELETE"



    def is_image(self):
        fileName, fileExtension = os.path.splitext(self.name.lower())

        if fileExtension in ['.jpg', '.png', '.jpeg', '.bmp']:
            return True

        return False


    def get_file(self):
        if self.type != None:
            # POST an image
            if self.type.startswith('image'):
                return {"name": self.name,
                        "type": self.type,
                        "size": self.size,
                        "upload_date":self.upload_date, 
                        "url": self.url, 
                        "thumbnailUrl": self.thumbnail_url,
                        "deleteUrl": self.delete_url, 
                        "deleteType": self.delete_type,}
            
            # POST an normal file
            elif self.not_allowed_msg == '':
                return {"name": self.name,
                        "type": self.type,
                        "size": self.size, 
                        "upload_date":self.upload_date, 
                        "url": self.url, 
                        "iconUrl": self.iconurl,
                        "deleteUrl": self.delete_url, 
                        "deleteType": self.delete_type,}

            # File type is not allowed
            else:
                return {"error": self.not_allowed_msg,
                        "name": self.name,
                        "type": self.type,
                        "size": self.size,}

        # GET image from disk
        elif self.is_image():
            return {"name": self.name,
                    "size": self.size, 
                    "upload_date":self.upload_date, 
                    "url": self.url, 
                    "thumbnailUrl": self.thumbnail_url,
                    "deleteUrl": self.delete_url, 
                    "deleteType": self.delete_type,}
        
        # GET normal file from disk
        else:
            return {"name": self.name,
                    "size": self.size, 
                    "upload_date":self.upload_date, 
                    "url": self.url, 
                    "iconUrl": self.iconurl,
                    "deleteUrl": self.delete_url, 
                    "deleteType": self.delete_type,}
