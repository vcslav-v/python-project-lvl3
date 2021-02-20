"""Test fixtures."""
import pytest
import os

fixtures_path = os.path.join('tests', 'fixtures')


@pytest.fixture
def simple_html():
    with open(os.path.join(fixtures_path, 'simple.html')) as fixture_file:
        fixture_data = fixture_file.read()
    return fixture_data


@pytest.fixture
def res_test_html():
    with open(os.path.join(
        fixtures_path,
        'page_with_resources',
        'test.html',
    )) as fixture_file:
        fixture_data = fixture_file.read()
    return fixture_data


@pytest.fixture
def res_test_expect_html():
    with open(
        os.path.join(
            fixtures_path,
            'page_with_resources',
            'test_expect.html',
        )
    ) as fixture_file:
        fixture_data = fixture_file.read()
    return fixture_data


@pytest.fixture
def text_res_file_path_expect():
    with open(
        os.path.join(
            fixtures_path,
            'page_with_resources',
            'text_res_file_path_expect.txt',
        )
    ) as fixture_file:
        fixture_data = fixture_file.readlines()
    return fixture_data


@pytest.fixture
def img_res_file_path_expect():
    with open(
        os.path.join(
            fixtures_path,
            'page_with_resources',
            'img_res_file_path_expect.txt',
        )
    ) as fixture_file:
        fixture_data = fixture_file.readlines()
    return fixture_data


@pytest.fixture
def text_res_urls_expect():
    with open(os.path.join(
        fixtures_path,
        'page_with_resources',
        'text_urls.txt',
    )) as fixture_file:
        fixture_data = fixture_file.readlines()
    return fixture_data


@pytest.fixture
def img_res_urls_expect():
    with open(os.path.join(
        fixtures_path,
        'page_with_resources',
        'img_urls.txt',
    )) as fixture_file:
        fixture_data = fixture_file.readlines()
    return fixture_data


@pytest.fixture
def img_file():
    with open(os.path.join(
        fixtures_path,
        'page_with_resources',
        'img.jpg',
    ), 'rb') as fixture_file:
        fixture_data = fixture_file.read()
    return fixture_data
