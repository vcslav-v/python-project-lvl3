from page_loader.loader import download
from page_loader.parser import get_url_info, get_url_name
import os
import requests_mock
import tempfile
import pytest
from bs4 import BeautifulSoup


@pytest.mark.parametrize('url, expect', [
    ({
        'scheme': 'https://',
        'netloc': 'google.com',
        'path': '',
        'full_url': 'https://google.com'
    }, 'google-com'),
    ({
        'scheme': 'https://',
        'netloc': 'TeST.com',
        'path': '/index.html',
        'full_url': 'https://TeST.com/index.html'
    }, 'TeST-com-index'),
    ({
        'scheme': 'ftp://',
        'netloc': 'ru.wikipedia.org',
        'path': '/wiki/%D0%81',
        'full_url': 'ru.wikipedia.org/wiki/%D0%81'
    }, 'ru-wikipedia-org-wiki-D0-81'),
])
def test_get_url_name(url, expect):
    result = get_url_name(url)
    assert result == expect


@pytest.mark.parametrize('url, mock_url, content_type, data, expect_data', [
    (
        'http://google.com',
        'http://google.com',
        'text/html; charset=UTF-8',
        'test_html',
        'test_html'
    ),
    (
        'google.com',
        'http://google.com',
        'text/html',
        'test_html',
        'test_html'
    ),
    (
        'https://google.com/index.html',
        'https://google.com/index.html',
        'text/html',
        'test_html',
        'test_html',
    ),
    (
        'https://google.com/',
        'https://google.com/',
        'text/css',
        'test_html',
        'test_html',
    ),
])
def test_download(url, mock_url, content_type, data, expect_data, request):
    data = request.getfixturevalue(data)
    expect_data = request.getfixturevalue(expect_data)

    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mocker:
            mocker.get(mock_url, text=data, headers={
                'Content-Type': content_type
            })
            result_path = download(url, tmp_dir)
        expect_path = os.path.join(
            tmp_dir,
            get_url_name(get_url_info(url)) + '.html'
        )
        assert result_path == expect_path

        with open(result_path, 'r') as result_file:
            soup = BeautifulSoup(result_file.read(), 'lxml')

        expect_soup = BeautifulSoup(expect_data, 'lxml')
        assert soup.prettify(formatter='html5') == (
            expect_soup.prettify(formatter='html5')
        )


@pytest.mark.parametrize(
    'url, mock_url, content_type, status_code, error_type', [
        (
            'http://google.com',
            'http://google.com',
            'text/html',
            301,
            ConnectionError
        ),
    ]
)
def test_download_request_errors(
    url,
    mock_url,
    content_type,
    status_code,
    error_type
):
    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mocker:
            mocker.get(mock_url, headers={
                'Content-Type': content_type,
                }, status_code=status_code
            )
            with pytest.raises(error_type):
                download(url, tmp_dir)


def test_download_dir_not_exist():
    URL = 'test.com'
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(FileNotFoundError):
            download(URL, os.path.join(tmp_dir, 'temp'))


@pytest.mark.parametrize(
    (
        'url, html_data, expect_html_data, expect_res_path, ' +
        'expect_page_file_name, urls_res, expect_files'
    ),
    [
        (
            'http://site.com/blog/about',
            'hexlet_case_html',
            'hexlet_case_expect_html',
            'site-com-blog-about_files',
            'site-com-blog-about.html',
            'url_res_hexlet',
            'file_path_res_hexlet_expect',
        ),
    ]
)
def test_download_hexlet(
    url,
    html_data,
    expect_html_data,
    expect_res_path,
    expect_page_file_name,
    urls_res,
    expect_files,
    request
):
    html_data = request.getfixturevalue(html_data)
    expect_html_data = request.getfixturevalue(expect_html_data)
    urls_res = request.getfixturevalue(urls_res)
    expect_files = request.getfixturevalue(expect_files)
    expect_soup = BeautifulSoup(expect_html_data, 'html.parser')

    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mocker:
            mocker.get(url, text=html_data)
            for url_res in urls_res:
                mocker.get(url_res.strip(), text='img')
            result_path = download(url, tmp_dir)
        expect_path = os.path.join(
            tmp_dir,
            expect_page_file_name
        )
        assert result_path == expect_path

        with open(result_path, 'r') as result_file:
            soup = BeautifulSoup(result_file.read(), 'html.parser')
        expect_html = expect_soup.prettify(formatter='html5')
        result_html = soup.prettify(formatter='html5')
        assert expect_html == result_html
