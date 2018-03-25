from unittest import TestCase, main
from project.image_fetcher import image_fetcher


class TestImage_Fetcher(TestCase):


    def test_image_fetcher(self):
        artist = Metallica
        self.assertEqual(Metallica, image_fetcher(artist))
        




if __name__ == '__main__':
    main()
