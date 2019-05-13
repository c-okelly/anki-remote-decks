from setuptools import setup, find_packages

setup(name='anki-remote-decks',
      version='0.0.1',
      description='',
      author='Conor OKelly',
      author_email='okellyconor@gmail.com',
      url='https://github.com/c-okelly/anki-remote-decks',
      python_requires='>3.4',
      install_requires=['requests', 'bs4'],
      tests_require=['nose', 'coverage', 'jsonlib-python3'],
      test_suite="nose.collector",
      packages=find_packages(),
      include_package_data=True,
      )