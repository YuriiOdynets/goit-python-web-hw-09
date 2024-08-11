# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface

# # #from itemadapter import ItemAdapter


# ## class Homework9Pipeline:
# # #    def process_item(self, item, spider):
# # #        return item

import json
import os

class JsonWriterPipeline:

    def open_spider(self, spider):
        if spider.name == 'quotes':
            self.file = self.handle_file('quotes.json')
        elif spider.name == 'authors':
            self.file = self.handle_file('authors.json')
        self.first_item = True  

    def handle_file(self, filename):
        file_exists = os.path.exists(filename)

        if file_exists:
            file = open(filename, 'r+')
            file.seek(0, os.SEEK_END)  # Переміщаємось в кінець файлу
            if file.tell() > 1:  # Файл не порожній
                file.seek(file.tell() - 1)  # Переміщаємось перед закриваючою дужкою
                file.truncate()  # Видаляємо закриваючу дужку
                file.write(',\n')  # Додаємо кому перед новим об'єктом
            else:
                file.seek(0)
                file.write('[')  
        else:
            file = open(filename, 'w')
            file.write('[')  

        return file

    def close_spider(self, spider):
        self.file.write('\n]')  # Закриваємо масив у файлі
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)
        if not self.first_item:
            self.file.write(',\n')
        self.file.write(line)
        self.first_item = False  
        return item
