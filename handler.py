import json
import os

from classes.crawl import Crawl
from classes.crawl_result import CrawlResult
from classes.util import Util
from string import Template

uti = Util()

def list(event, contenxt):
    results = uti.get_all_saved_results()
    
    content = ""
    
    for result in results:
        content += "<li> " + result["title"] + "<br /><a href='" + result["s3_path"] + "'>" + result["page_name"] + "</a> Created: " + result["created"] +"<br />"
        content += "<p> Original Link:" + result['crawl_url'] + "</p>" 
        content += "</li></hr />"
    
    template = """
        <html>
        <head><title>Web Alert Results</title></head>
        <body>
            <h1>Web Alert Results</h1>
            <ul>
        """
    
    template += content

    template += """
            </ul>
        </body>
        </html>
        """
    
    html = template

    response = {
        "headers": {
            "Content-Type": "text/html",
        },
        "statusCode": 200,
        "body": html
    }

    return response
    
def crawl(event, context):
    
    alerts = json.loads(open('./urls.json', 'r').read())["alert"]
    
    for alert in alerts:
        for key in alert:
            crawl = Crawl(key, alert[key])
            crawl.fetch()
    body = {
        "message": "success",
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "success",
    }
    """


# fetch page
# if page has results   
#     check dynamoddb
#         if results
#             do nothing
#         else:
#             gather links
#             save html from links to s3
#             alert me
# else:
#     do nothing