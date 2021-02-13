from page_loader.localizer import localize_resources
import requests_mock
import os
import tempfile
import pytest
from bs4 import BeautifulSoup


@pytest.mark.parametrize(
    'url, test_data, mock_img_urls, expect_data, expect_img_files', [
        (
            {
                'scheme': 'http://',
                'netloc': 'test.com',
                'path': '',
                'full_url': 'http://test.com',
                'file_name': 'test-com',
                'res_dir_name': 'test-com_files',
                'assets_prefix': 'test-com',
            },
            'res_test_html',
            'res_urls',
            'res_test_expect_html',
            'res_file_path_expect',
        ),
    ]
)
def test_dowload_resources(
    url,
    test_data,
    mock_img_urls,
    expect_data,
    expect_img_files,
    request
):
    data = request.getfixturevalue(test_data)
    mock_img_urls = request.getfixturevalue(mock_img_urls)
    expect_data = request.getfixturevalue(expect_data)
    expect_img_files = request.getfixturevalue(expect_img_files)
    expect_soup = BeautifulSoup(expect_data, 'lxml')
    url['data'] = data

    with tempfile.TemporaryDirectory() as tmp_dir:
        resources_output_path = os.path.join(tmp_dir, url['res_dir_name'])
        with requests_mock.Mocker() as mocker:
            for img_url in mock_img_urls:
                mocker.get(img_url.strip(), text='img')
            result_html = localize_resources(url, tmp_dir)

        assert os.path.exists(resources_output_path) and (
            os.path.isdir(resources_output_path)
        )
        for path_file in expect_img_files:
            assert os.path.exists(os.path.join(
                resources_output_path,
                path_file.strip()
            ))

    soup = BeautifulSoup(result_html, 'lxml')

    expect_html = expect_soup.prettify(formatter='html5')
    result_html = soup.prettify(formatter='html5')
    assert result_html == expect_html
