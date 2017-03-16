from setuptools import setup

setup(name='org_tree',
      version='1.0',
      description='Draw org files as graphs',
      url='http://github.com/storborg/funniest',
      author='Gabriele Muciaccia',
      author_email='crash@inventati.org',
      license='MIT',
      packages=['org_tree'],
      install_requires=[
        "networkx",
        "plotly",
      ],
      zip_safe=False)
