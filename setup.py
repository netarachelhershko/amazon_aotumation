from setuptools import setup

setup(name='amazon_automation',
      version='1.0',
      description='Amazon Automation Porject',
      url='http://github.com/netarachelhershko/amazon_automation',
      author='Neta Hershko',
      author_email='netarachelhershko@gmail.com',
      license='MIT',
      packages=[],
      install_requires=[
          'python-wordpress-xmlrpc',
          'bitly_api',
          'requests',
          'BeautifulSoup',
          'python-amazon-product-api',
          'lxml', 'tldextract'
      ],
      zip_safe=False)
