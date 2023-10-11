import unittest

import Product

# terminal command: 
# python -m unittest test/ProductTest.py

class Test(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """


    # Check that retailer ID has been generated correctly
    def test_retailer_id_is_not_None(self):
        print("Start test_retailer_id_is_not_None test\n")
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        retailer = Product.Retailer(retailer="Test Retailer", country="Canada", currency="CAD")  # instantiate the Retailer Class

        self.assertIsNotNone(retailer.retailer_id)

    
    def test_retailer_id_is_correct(self):
        print("Start test_retailer_id_is_correct test\n")
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        retailer = Product.Retailer(retailer="Test Retailer", country="Canada", currency="CAD")  # instantiate the Retailer Class
        retailer2 = Product.Retailer(retailer="Test Retailer2", country="Canada", currency="CAD")  # instantiate the Retailer Class
        retailer3 = Product.Retailer(retailer="Test Retailer", country="USA", currency="USD")  # instantiate the Retailer Class

        self.assertEqual(retailer.retailer_id, "886a3c0ff8ae84dfe9d1ba52ffe2d0bf738e4917")
        self.assertNotEqual(retailer2.retailer_id, "886a3c0ff8ae84dfe9d1ba52ffe2d0bf738e4917")
        self.assertEqual(retailer3.retailer_id, "886a3c0ff8ae84dfe9d1ba52ffe2d0bf738e4917")

    def test_retailer_validate_function(self):
        print("Start test_retailer_validate_function test\n")
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        retailer1 = Product.Retailer(retailer="Test Retailer", country="Canada", currency="CAD")  # instantiate the Retailer Class
        retailer2 = Product.Retailer(retailer="Test Retailer", country="Canada", currency="CAD")  # instantiate the Retailer Class

        retailer1.products = [1]

        self.assertEqual(retailer1.validate(), True) # all data attributes not None
        self.assertEqual(retailer2.validate(), False) # missing data


    def test_product_get_gender_function(self):
        print("Start test_retailer_validate_function test\n")
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        product = Product.Product()
        product2 = Product.Product()
        product3 = Product.Product()

        product.scraped_product_name = "Vapor V Women's"
        product2.scraped_product_name = "Drago Climbing Shoes"
        product3.scraped_product_name = "Men's Origin"

        product.getGender()
        product2.getGender()
        product3.getGender()

        self.assertEqual(product.gender,"f")
        self.assertEqual(product.formatted_product_name,"vapor v")

        self.assertEqual(product2.gender,"u")
        self.assertEqual(product2.formatted_product_name,"drago")

        self.assertEqual(product3.gender,"m")
        self.assertEqual(product3.formatted_product_name,"origin")

    
    def test_product_match_brand_function(self):
        print("Start test_product_match_brand_function test\n")
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        product = Product.Product()

        product.scraped_brand = "La Sportiva"
        product.getMatchedBrand()
        self.assertEqual(product.matched_brand,"la sportiva")


        product.scraped_brand = "La Sportiva Climbing"
        product.getMatchedBrand()
        self.assertEqual(product.matched_brand,"la sportiva")

        product.scraped_brand = "La Sportiva -"
        product.getMatchedBrand()
        self.assertEqual(product.matched_brand,"la sportiva")

        product.scraped_brand = "Sportiva"
        product.getMatchedBrand()
        self.assertEqual(product.matched_brand,"la sportiva")

        product.scraped_brand = "La Scarpa"
        product.getMatchedBrand()
        self.assertEqual(product.matched_brand,"scarpa")

    def test_product_match_product_name_function(self):
        print("Start test_product_match_product_name_function test\n")
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        product = Product.Product()
        product.scraped_brand = "Unparallel"

        product.scraped_product_name = "TN Pro"
        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        self.assertEqual(product.matched_product_name,"tn pro")

        product.scraped_product_name = "TN Pro Climbing Shoes"
        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        self.assertEqual(product.matched_product_name,"tn pro")

        product.scraped_product_name = "TN Pros"
        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        self.assertEqual(product.matched_product_name,"tn pro")

        product.scraped_product_name = "TN Pro -"
        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        self.assertEqual(product.matched_product_name,"tn pro")

        product.scraped_product_name = "tn pro lv"
        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        self.assertEqual(product.matched_product_name,"tn pro lv")


    def test_product_validate_function(self):
        print("Start test_product_validate_function test\n")
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        product = Product.Product()
        product2 = Product.Product()

        product.id = "123"
        product.web_url = "test.com"
        product.matched_brand = "scarpa"
        product.scraped_brand = "Scarpa"
        product.matched_product_name = "drago"
        product.formatted_product_name = "drago"
        product.scraped_product_name = "Drago"
        product.gender = 'u'
        product.og_price = 239.99
        product.sale_price = 209.99
        product.discount_pct = 20


        self.assertEqual(product.validate(), True) # all data attributes not None
        self.assertEqual(product2.validate(), False) # missing data


    def test_product_generate_id_function(self):
        print("Start test_product_generate_id_function test\n")
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        retailer = Product.Retailer("Test", "Canada", "CAD")

        product = Product.Product()
        product2 = Product.Product()

        product.id = None
        product.web_url = "test.com"
        product.matched_brand = "scarpa"
        product.scraped_brand = "Scarpa"
        product.matched_product_name = "drago"
        product.formatted_product_name = "drago"
        product.scraped_product_name = "Drago"
        product.gender = 'u'
        product.og_price = 239.99
        product.sale_price = 209.99
        product.discount_pct = 20

        product.generateID(retailer)
        product2.generateID(retailer)


        self.assertIsNotNone(product.id) # all data attributes not None
        self.assertIsNone(product2.id) # missing data

if __name__ == "__main__":
    unittest.main()