from page_loader.loader import download, make_file_name, prepare_url
import os
import requests_mock
import tempfile
import pytest


@pytest.mark.parametrize('url, content_type , expect', [
    ('https://google.com', 'text/html; charset=ISO-8859-1', 'google-com.html'),
    (
        'https://TeST.com/index.html',
        'text/html',
        'TeST-com-index.html'
    ),
    (
        'ftp://ru.wikipedia.org/wiki/%D0%81',
        'text/html; charset=UTF-8',
        'ru-wikipedia-org-wiki-D0-81.html'
    ),
])
def test_make_file_name(url, content_type, expect):
    result = make_file_name(url, content_type)
    assert result == expect


@pytest.mark.parametrize('url, content_type, error_type', [
    ('http://google.com/', 'text/css', ValueError)
])
def test_make_file_name_errors(url, content_type, error_type):
    with pytest.raises(error_type):
        make_file_name(url, content_type)


@pytest.mark.parametrize('url, mock_url, content_type, body', [
    ('http://google.com', 'http://google.com', 'text/html', 'data'),
    ('google.com', 'http://google.com', 'text/html', 'data'),
    (
        'https://google.com/index.html',
        'https://google.com/index.html',
        'text/html',
        'data'
    ),
])
def test_download(url, mock_url, content_type, body):
    with tempfile.TemporaryDirectory() as tmp_dir:
        with requests_mock.Mocker() as mocker:
            mocker.get(mock_url, text=body, headers={
                'Content-Type': 'text/html'
            })
            result_path = download(url, tmp_dir)
        expect_path = os.path.join(
            tmp_dir,
            make_file_name(prepare_url(url), 'text/html')
        )
        assert result_path == expect_path

        with open(result_path, 'r') as result_file:
            assert body == result_file.read()


@pytest.mark.parametrize(
    'url, mock_url, content_type, status_code, error_type', [
        (
            'http://google.com',
            'http://google.com',
            'text/html',
            301,
            ConnectionError
        ),
        (
            'googlecom',
            'http://google.com',
            'text/html',
            200,
            ValueError
        ),

    ]
)
def test_download_net_errors(
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
