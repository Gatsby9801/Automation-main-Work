from itertools import chain
import re

def test_flatten_list():
    main_list = [['umesh', 'nabin'], ['bikash'], ['dia', 'radu', 'ali'], ['tejas', 'narendra']]
    flatten_list = list(chain.from_iterable(main_list))
    print("final list " + str(flatten_list))


files = [
  "index.php.topic,390.0.html.txt",
  "index.php.topic,3.0.html.txt",
  "index.php.board=398.0.html.txt",
  "index.php.topic,401.0.html.txt",
  "index.php.topic,45.txt",
  "index.php.topic=4.0.txt",
  "index.php.board=430.15.txt",
  "index.php.topic=14.30.txt",
  "index.php.topic=372.45.txt",
  "index.php.topic=5.0.txt",
]

def test_find_topic():
    i = [i for i in files if "index" in files]
    print(i)

def test_regualr_expression():
    phoneNumRegex = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')
    mo = phoneNumRegex.search('Cell: 415-555-9999 Work: 212-555-0000')
    mo.group()
    print('success!!')