from setuptools import setup, find_packages
import sys, os

setup(name='django-chainviews',
    version=__import__('chainviews').__version__,
    description="'Chain Views' for django",
    long_description=""" """,
    # Get more strings from http://www.python.org/pypi?:action=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='',
    author='corey jergensen',
    author_email='corey.jergensen@gmail.com',
    url='',
    license='',
    packages=[
        'chainviews',
    ],
    package_dir={'chainviews': 'chainviews',},
    include_package_data=True,
    install_requires=[
      # -*- Extra requirements: -*-
    ],
)
