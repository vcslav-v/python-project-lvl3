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
def res_file_path_expect():
    with open(
        os.path.join(
            fixtures_path,
            'page_with_resources',
            'file_path_expect.txt',
        )
    ) as fixture_file:
        fixture_data = fixture_file.readlines()
    return fixture_data


@pytest.fixture
def res_urls():
    with open(os.path.join(
        fixtures_path,
        'page_with_resources',
        'urls.txt',
    )) as fixture_file:
        fixture_data = fixture_file.readlines()
    return fixture_data


@pytest.fixture
def res_test_2_html():
    with open(os.path.join(
        fixtures_path,
        'page_with_resources_2',
        'test.html',
    )) as fixture_file:
        fixture_data = fixture_file.read()
    return fixture_data


@pytest.fixture
def res_test_2_expect_html():
    with open(
        os.path.join(
            fixtures_path,
            'page_with_resources_2',
            'test_expect.html',
        )
    ) as fixture_file:
        fixture_data = fixture_file.read()
    return fixture_data


@pytest.fixture
def res_file_path_expect_2():
    with open(
        os.path.join(
            fixtures_path,
            'page_with_resources_2',
            'file_path_expect.txt',
        )
    ) as fixture_file:
        fixture_data = fixture_file.readlines()
    return fixture_data


@pytest.fixture
def res_urls_2():
    with open(os.path.join(
        fixtures_path,
        'page_with_resources_2',
        'urls.txt',
    )) as fixture_file:
        fixture_data = fixture_file.readlines()
    return fixture_data
