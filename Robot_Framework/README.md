# Automation
1. Install python if not installed in your machine
2. Checkout this repo
3. Install requirements: 
	  - $ pip install robotframework
	  - $ pip install selenium
	  - $ pip install --upgrade robotframework-seleniumlibrary
	  - $ pip install --upgrade robotframework-selenium2library
	  - $ pip install --upgrade robotframework-appiumlibrary
4. Go to the project folder from command line e.g. cd /Users/Something/Projects/Automation
5. Check your chrome browser's version and download the chromedriver from site: https://chromedriver.chromium.org/downloads
6. Put the chromedriver file inside Automation/Driver folder
7. Run command:
    i) Run Prjoject: robot -d ../Output/ test.robot 
      - After completion,open report.html to see the detail report.
      
NOTE: For mobile app test cases to run, you need to setup environmemt for Appium automation with Robot Framework e.g. Appium, Android studio, Android sdk, Java etc..
