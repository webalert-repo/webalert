import os
import re
import urllib2
import boto3
import datetime
from bs4 import BeautifulSoup
from boto3.dynamodb.conditions import Key, Attr

class Util():
    def __init__(self):
        self.s3 = boto3.resource('s3')
        self.db = boto3.resource("dynamodb")
        self.dynamodb_table = os.environ['DYNAMODB_TABLE'] 
        self.region = os.environ['REGION'] 
        self.s3_bucket = os.environ['S3_BUCKET'] 
        return
    def log_error(self, err):
        print err
    def upload_files(self, filename, bucket, data, content_type):
            try:
                upload = self.s3.Object(bucket, filename)
                upload.put(Body=data, ContentType=content_type)
                return True
            except Exception as err:
                self.log_error(err)
                return False
    def get_all_css(self, soup_body, folder_path):
        links = soup_body.find_all('link')
        for link in links:
            href = 'https:' + link.get('href')
            filename = href.split('/').pop().split('?')[0]
            file_type = filename.split('.').pop()
            if('css' in file_type):
                link['href'] = filename.split('?')[0]
                request = urllib2.Request(href)
                css = urllib2.urlopen(request).read()
                self.upload_files(folder_path + '/' + filename, self.s3_bucket, css, 'text/css')  
    def get_all_images(self, soup_body, folder_path):
        print 'getting all images...'
        images = soup_body.find_all('img')
        for image in images:
            src = image.get('src')
            filename = src.split('/').pop()
            image['src'] = filename
            request = urllib2.Request(src)
            img = urllib2.urlopen(request).read()
            content_type = 'image/' + filename.split('.').pop()
            self.upload_files(folder_path + '/' + filename, self.s3_bucket, img, content_type)  
    def save_html(self, soup_body, folder_path):
        full_path = folder_path + '/' + 'index.html'
        s3_path = 'https://s3-' + self.region + '.amazonaws.com/' + self.s3_bucket + '/' + full_path
        print 'Saving HTML: ' + s3_path
        self.upload_files(full_path, self.s3_bucket, soup_body.prettify('utf-8'),'text/html')
        return s3_path
    def get_all_saved_results(self):
            table = self.db.Table(self.dynamodb_table)
            result = table.scan()
            return result['Items']
    def check_duplicate(self, page_name):
        try:
            table = self.db.Table(self.dynamodb_table)
            result = table.get_item(
                Key = {
                    'page_name': page_name
                }
            )
            print len(result['Item'])
            if(result['Item'] and result['Item']['page_name']):
                print page_name, ' already exists'
                return True
            return False
        except Exception as err:
            self.log_error(err)
      
    def save_results_db(self, details):
        table = self.db.Table(self.dynamodb_table)
        result = table.put_item(Item = {
            'page_name': details.page_name,
            'title': details.title,
            's3_path': details.s3_path,
            'crawl_url': details.crawl_url,
            'keyword': details.keyword,
            'created': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
        return
    def fetch_crawl_url(self, crawl_url):
        request = urllib2.urlopen(crawl_url).read()
        return BeautifulSoup(request, "html.parser")
    def make_folder(self, fpath):
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        return