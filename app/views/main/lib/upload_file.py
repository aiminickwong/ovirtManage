# -*- coding:utf-8 -*-

import os

class uploadfile():
    def __init__(self, name, type=None, size=None, not_allowed_msg=''):
        self.name = name
        self.type = type
        self.size = size
        #self.upload_date = upload_date
        self.not_allowed_msg = not_allowed_msg
        self.url = "data/%s" % name
        #self.thumbnail_url = "thumbnail/%s" % name  获取每张缩略图
        self.thumbnail_url = "thumbnail/Picture_icon.png" 
        self.iconurl = "thumbnail/ISO_ICON.png"
        self.delete_url = "delete/%s" % name
        self.delete_type = "DELETE"



    def is_image(self):
        fileName, fileExtension = os.path.splitext(self.name.lower())

        if fileExtension in ['.jpg', '.png', '.jpeg', '.bmp']:
            return True

        return False


    def get_file(self):
        if self.type != None:
            # POST an image                  这里的self.not_allowed_msg == ''要特别注意
            if self.type.startswith('image') and self.not_allowed_msg == '':
                return {"name": self.name,
                        "type": self.type,
                        "size": self.size,
                        #"upload_date":self.upload_date, 
                        "url": self.url, 
                        "thumbnailUrl": self.thumbnail_url,
                        "deleteUrl": self.delete_url, 
                        "deleteType": self.delete_type,}
            
            # POST an normal file
            elif self.not_allowed_msg == '':
                return {"name": self.name,
                        "type": self.type,
                        "size": self.size, 
                        #"upload_date":self.upload_date, 
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
                    #"upload_date":self.upload_date, 
                    "url": self.url, 
                    "thumbnailUrl": self.thumbnail_url,
                    "deleteUrl": self.delete_url, 
                    "deleteType": self.delete_type,}
        
        # GET normal file from disk
        else:
            return {"name": self.name,
                    "size": self.size, 
                    #"upload_date":self.upload_date, 
                    "url": self.url, 
                    "iconUrl": self.iconurl,
                    "deleteUrl": self.delete_url, 
                    "deleteType": self.delete_type,}
