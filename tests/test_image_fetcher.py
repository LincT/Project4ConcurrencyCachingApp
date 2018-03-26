from unittest import TestCase, main
from project.image_fetcher import image_fetcher


class TestImage_Fetcher(TestCase):
    # Test the api call output.
    def test_fetch_output(self):
        artist = 'michael jackson'
        image_url = image_fetcher.fetch(self, artist)
        expected = 'https://upload.wikimedia.org/wikipedia/commons/3/32/1993_walk_of_fame_michael_jackson.jpg'
        self.assertEqual(expected, image_url)

if __name__ == '__main__':
    main()
