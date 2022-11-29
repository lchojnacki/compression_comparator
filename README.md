# Comparison of compression standards

The most popular compression standard on the Internet is gzip. It is widely
supported by browsers and other clients (such as 
[requests](https://pypi.org/project/requests/)).

In 2015, Facebook released [zstandard](https://pypi.org/project/zstandard/), 
a new lossless compression standard that features better compression rates and 
faster performance than gzip.

## Usage

Tested on Python 3.10.

Install requirements:

    pip install -r requirements.txt

Compare compression standards for unified data:

    python comparator.py compare_unified --length 1000

Compare compression standards for random data:

    python comparator.py compare_random --length 1000

Compare compression standards for a specific file:

    python comparator.py compare_file --path path/to/file.txt
