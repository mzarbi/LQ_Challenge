# project/server/tests/test_main.py


import unittest
from unittest import TestCase


class TestMainBlueprint(TestCase):

    def test_index(self):
        # Ensure Flask is setup.
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
