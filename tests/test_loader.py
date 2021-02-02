from page_loader.loader import download, prepare_url, normalize_name
import os
import requests_mock
import tempfile
import pytest


@pytest.mark.parametrize('url, expect', [
    ('https://google.com', 'google-com'),
    ('https://TeST.com/index.html', 'TeST-com-index'),
    ('ftp://ru.wikipedia.org/wiki/%D0%81', 'ru-wikipedia-org-wiki-D0-81'),
])
def test_make_file_name(url, expect):
    result = normalize_name(url)
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
        'text/html',
        'img_test_html',
        'img_test_html',
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
            normalize_name(prepare_url(url)) + '.html'
        )
        assert result_path == expect_path

        with open(result_path, 'r') as result_file:
            assert expect_data == result_file.read()


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
        (
            'http://google.com',
            'http://google.com',
            'text/css',
            200,
            ValueError
        ),

    ]
)
def test_download_errors(
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
