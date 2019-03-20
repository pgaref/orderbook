from setuptools import setup, find_packages

setup(name='orderbook',
      description='Python LimitOrderBook',
      url="https://github.com/pgaref/orderbook",
      version='1.1.2',
      author='Panagiotis Garefalakis',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      platforms='any',
      scripts=['bin/runner.py'])