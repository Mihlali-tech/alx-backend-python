#!/usr/bin/env python3
"""Test module for client.GithubOrgClient"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected, mock_get_json):
        """Test that org returns the correct value"""
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct value"""
        with patch.object(
            GithubOrgClient, 'org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }
            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/google/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct list of repos"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        with patch.object(
            GithubOrgClient, '_public_repos_url', new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the correct boolean"""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class method to mock requests.get"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Side effect function to return different payloads based on URL"""
            if url.endswith('/orgs/google'):
                return Mock(json=lambda: cls.org_payload)
            if url.endswith('/orgs/google/repos'):
                return Mock(json=lambda: cls.repos_payload)
            return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos_integration(self):
        """Test public_repos with integration"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license_integration(self):
        """Test public_repos with license filter in integration"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""
    
    @classmethod
    def setUpClass(cls):
        """Mock requests.get to return payloads based on URL"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        
        def side_effect(url):
            if url.endswith("/orgs/google"):
                return Mock(json=lambda: cls.org_payload)
            elif url.endswith("/orgs/google/repos"):
                return Mock(json=lambda: cls.repos_payload)
            return None
        
        cls.mock_get.side_effect = side_effect
    
    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()
    
    def test_public_repos_integration(self):
        """Test public_repos without license filter"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)
    
    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )