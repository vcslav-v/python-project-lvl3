from page_loader.localizer import download_resources
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
                'res_folder_name': 'test-com_files'
            },
            'res_test_html',
            'url_res',
            'res_test_expect_html',
            'file_path_res_expect',
        )
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

    with tempfile.TemporaryDirectory() as tmp_dir:
        resources_output_path = os.path.join(tmp_dir, url['res_folder_name'])
        with requests_mock.Mocker() as mocker:
            for img_url in mock_img_urls:
                mocker.get(img_url.strip(), text='img')
            result_html = download_resources(data, url, tmp_dir)

        assert os.path.exists(resources_output_path) and (
            os.path.isdir(resources_output_path)
        )
        for path_file in expect_img_files:
            assert os.path.exists(os.path.join(
                resources_output_path,
                path_file.strip()
            ))

    soup = BeautifulSoup(result_html, 'lxml')

    assert soup.prettify(formatter='html5') == (
        expect_soup.prettify(formatter='html5')
    )
