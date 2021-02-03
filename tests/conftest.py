"""Test fixtures."""
import pytest
import os

fixtures_path = os.path.join('tests', 'fixtures')


@pytest.fixture
def test_html():
    with open(os.path.join(fixtures_path, 'test.html')) as fixture_file:
        fixture_data = fixture_file.read()
    return fixture_data


@pytest.fixture
def res_test_html():
    with open(os.path.join(fixtures_path, 'res_test.html')) as fixture_file:
        fixture_data = fixture_file.read()
    return fixture_data


@pytest.fixture
def res_test_expect_html():
    with open(
        os.path.join(fixtures_path, 'res_test_expect.html')
    ) as fixture_file:
        fixture_data = fixture_file.read()
    return fixture_data


@pytest.fixture
def file_path_res_expect():
    with open(
        os.path.join(fixtures_path, 'file_path_res_expect.txt')
    ) as fixture_file:
        fixture_data = fixture_file.readlines()
    return fixture_data


@pytest.fixture
def url_res():
    with open(os.path.join(fixtures_path, 'url_res.txt')) as fixture_file:
        fixture_data = fixture_file.readlines()
    return fixture_data
