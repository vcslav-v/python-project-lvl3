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
def img_test_html():
    with open(os.path.join(fixtures_path, 'img_test.html')) as fixture_file:
        fixture_data = fixture_file.read()
    return fixture_data


@pytest.fixture
def img_test_expect_html():
    with open(
        os.path.join(fixtures_path, 'img_test_expect.html')
    ) as fixture_file:
        fixture_data = fixture_file.read()
    return fixture_data
