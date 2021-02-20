from page_loader.loader import download, errors
import os
import requests_mock
import tempfile
import pytest
from bs4 import BeautifulSoup


@pytest.mark.parametrize(
    'url, mock_url, html_file_expect, content_type, data, expect_data', [
        (
            'http://google.com',
            'http://google.com',
            'google-com.html',
            'text/html; charset=UTF-8',
            'simple_html',
            'simple_html'
        ),
        (
            'google.com',
            'http://google.com',
            'google-com.html',
            'text/html',
            'simple_html',
            'simple_html'
        ),
        (
            'https://google.com/index.html',
            'https://google.com/index.html',
            'google-com-index.html',
            'text/html',
            'simple_html',
            'simple_html',
        ),
        (
            'https://google.com/',
            'https://google.com/',
            'google-com.html',
            'text/css',
            'simple_html',
            'simple_html',
        ),
    ]
)
def test_download(
    url,
    mock_url,
    html_file_expect,
    content_type,
    data,
    expect_data,
    request
):
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
            html_file_expect,
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
            501,
            errors.NetError
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
        with pytest.raises(errors.SaveError):
            download(URL, os.path.join(tmp_dir, 'temp'))


@pytest.mark.parametrize(
    (
        'url, html_data, expect_html_data, expect_res_path, '
        'expect_page_file_name, text_res_urls, img_res_urls, '
        'img, text_expect_files, img_expect_files'
    ),
    [
        (
            'http://site.com/blog/about',
            'res_test_html',
            'res_test_expect_html',
            'site-com-blog-about_files',
            'site-com-blog-about.html',
            'text_res_urls_expect',
            'img_res_urls_expect',
            'img_file',
            'text_res_file_path_expect',
            'img_res_file_path_expect',
        ),
    ]
)
def test_download_hexlet(
    url,
    html_data,
    expect_html_data,
    expect_res_path,
    expect_page_file_name,
    text_res_urls,
    img_res_urls,
    img,
    text_expect_files,
    img_expect_files,
    request
):
    html_data = request.getfixturevalue(html_data)
    expect_html_data = request.getfixturevalue(expect_html_data)
    text_res_urls = request.getfixturevalue(text_res_urls)
    img_res_urls = request.getfixturevalue(img_res_urls)
    img = request.getfixturevalue(img)
    text_expect_files = request.getfixturevalue(text_expect_files)
    img_expect_files = request.getfixturevalue(img_expect_files)
    expect_soup = BeautifulSoup(expect_html_data, 'html.parser')

    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mocker:
            mocker.get(url, text=html_data)
            for url_res in text_res_urls:
                mocker.get(url_res.strip(), text=html_data)
            for url_res in img_res_urls:
                mocker.get(url_res.strip(), content=img)
            result_path = download(url, tmp_dir)
        expect_path = os.path.join(
            tmp_dir,
            expect_page_file_name
        )
        assert result_path == expect_path

        expect_res_folder = os.path.join(tmp_dir, expect_res_path)
        assert os.path.isdir(expect_res_folder)

        for text_expect_file in text_expect_files:
            res_path = os.path.join(
                expect_res_folder, text_expect_file.strip()
            )
            assert os.path.exists(res_path)

            with open(res_path) as res_file:
                assert html_data == res_file.read()

        for img_expect_file in img_expect_files:
            res_path = os.path.join(expect_res_folder, img_expect_file.strip())
            assert os.path.exists(res_path)

            with open(res_path, 'rb') as res_file:
                assert img == res_file.read()

        with open(result_path, 'r') as result_file:
            soup = BeautifulSoup(result_file.read(), 'html.parser')
        expect_html = expect_soup.prettify(formatter='html5')
        result_html = soup.prettify(formatter='html5')
        assert expect_html == result_html
