import re
from typing import Self
import requests
import simplejson as json

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.chrome.options import Options as ChromeOptions

USERNAME_ACCESS_KEY = re.compile('^(http|https):\/\/([^:]+):([^@]+)@')


def report_sauce_status(name, status, tags=[], remote_url=''):
    # Parse username and access_key from the remote_url
    assert USERNAME_ACCESS_KEY.match(remote_url), 'Incomplete remote_url.'
    username, access_key = USERNAME_ACCESS_KEY.findall(remote_url)[0][1:]

    # Get selenium session id from the keyword library
    selenium = BuiltIn().get_library_instance('Selenium2Library')
    job_id = selenium._current_browser().session_id

    # Prepare payload and headers
    token = (':'.join([username, access_key])).encode('base64').strip()
    payload = {'name': name,
               'passed': status == 'PASS',
               'tags': tags}
    headers = {'Authorization': 'Basic {0}'.format(token)}

    # Put test status to Sauce Labs
    url = 'https://saucelabs.com/rest/v1/{0}/jobs/{1}'.format(username, job_id)
    response = requests.put(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200, response.text

    # Log video url from the response
    video_url = json.loads(response.text).get('video_url')
    if video_url:
        logger.info('<a href="{0}">video.flv</a>'.format(video_url), html=True)


def desired_cap():
    
    options = ChromeOptions()
    options.browser_version = 'latest'
    options.platform_name = 'Windows 10'
    sauce_options = {}
    
    sauce_options['name'] = 'FP Automation'
    sauce_options['screenResolution'] = '1920x1080'
    options.set_capability('sauce:options', sauce_options)
    

   
def setUp():

        Self.driver = webdriver.Remote(
            command_executor='http://$USERNAME:$ACCESS_KEY@ondemand.saucelabs.com:80/wd/hub',
            desired_capabilities={
                requests.options = ChromeOptions()
                options.browser_version = 'latest'
                options.platform_name = 'Windows 10'
                sauce_options = {}
    
                sauce_options['name'] = 'FP Automation'
                sauce_options['screenResolution'] = '1920x1080'
                options.set_capability('sauce:options', sauce_options)
            }
        )