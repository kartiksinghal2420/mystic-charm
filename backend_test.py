#!/usr/bin/env python3
"""
Backend API Testing for Lucky Charm Store
Tests all product-related endpoints and sample data initialization
"""

import requests
import json
import sys
from typing import Dict, List, Any
import os
from pathlib import Path

# Load environment variables to get the backend URL
def load_env_file(file_path: str) -> Dict[str, str]:
    """Load environment variables from .env file"""
    env_vars = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value.strip('"')
    return env_vars

# Get backend URL from frontend .env file
frontend_env = load_env_file('/app/frontend/.env')
BACKEND_URL = frontend_env.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"Testing backend at: {API_BASE_URL}")

class LuckyCharmAPITester:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str, details: Any = None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'details': details
        })
    
    def test_root_endpoint(self):
        """Test the root API endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "Lucky Charms Store API" in data["message"]:
                    self.log_test("Root Endpoint", True, "API root endpoint responding correctly")
                    return True
                else:
                    self.log_test("Root Endpoint", False, "Unexpected response format", data)
                    return False
            else:
                self.log_test("Root Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Connection error: {str(e)}")
            return False
    
    def test_get_products(self):
        """Test GET /api/products endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/products")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list) and len(products) > 0:
                    # Verify sample data structure
                    sample_product = products[0]
                    required_fields = ['id', 'name', 'description', 'price', 'category', 'image_url', 
                                     'spiritual_benefits', 'materials', 'featured', 'in_stock']
                    
                    missing_fields = [field for field in required_fields if field not in sample_product]
                    if not missing_fields:
                        self.log_test("Get Products", True, f"Retrieved {len(products)} products with correct structure")
                        return True, products
                    else:
                        self.log_test("Get Products", False, f"Missing fields in product: {missing_fields}", sample_product)
                        return False, []
                else:
                    self.log_test("Get Products", False, "No products found or invalid response format", products)
                    return False, []
            else:
                self.log_test("Get Products", False, f"HTTP {response.status_code}", response.text)
                return False, []
        except Exception as e:
            self.log_test("Get Products", False, f"Connection error: {str(e)}")
            return False, []
    
    def test_product_search(self):
        """Test product search functionality"""
        search_terms = ["crystal", "amethyst", "spiritual", "rose"]
        
        for term in search_terms:
            try:
                response = self.session.get(f"{self.base_url}/products", params={"search": term})
                if response.status_code == 200:
                    products = response.json()
                    if isinstance(products, list):
                        # Check if search results contain the search term
                        relevant_results = []
                        for product in products:
                            if (term.lower() in product.get('name', '').lower() or 
                                term.lower() in product.get('description', '').lower() or
                                any(term.lower() in benefit.lower() for benefit in product.get('spiritual_benefits', []))):
                                relevant_results.append(product)
                        
                        if len(relevant_results) > 0:
                            self.log_test(f"Search '{term}'", True, f"Found {len(relevant_results)} relevant products")
                        else:
                            self.log_test(f"Search '{term}'", False, f"No relevant results for '{term}'", products)
                    else:
                        self.log_test(f"Search '{term}'", False, "Invalid response format", products)
                else:
                    self.log_test(f"Search '{term}'", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_test(f"Search '{term}'", False, f"Connection error: {str(e)}")
    
    def test_category_filtering(self):
        """Test category filtering"""
        categories = ["crystals", "spiritual_jewelry", "healing_stones", "amulets", "talismans", "protection_charms"]
        
        for category in categories:
            try:
                response = self.session.get(f"{self.base_url}/products", params={"category": category})
                if response.status_code == 200:
                    products = response.json()
                    if isinstance(products, list):
                        # Verify all products belong to the requested category
                        correct_category = all(product.get('category') == category for product in products)
                        if correct_category:
                            self.log_test(f"Category '{category}'", True, f"Found {len(products)} products in category")
                        else:
                            wrong_categories = [p.get('category') for p in products if p.get('category') != category]
                            self.log_test(f"Category '{category}'", False, f"Found products with wrong categories: {wrong_categories}")
                    else:
                        self.log_test(f"Category '{category}'", False, "Invalid response format", products)
                else:
                    self.log_test(f"Category '{category}'", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_test(f"Category '{category}'", False, f"Connection error: {str(e)}")
    
    def test_featured_products(self):
        """Test featured products endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/featured-products")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list):
                    # Verify all products are marked as featured
                    all_featured = all(product.get('featured', False) for product in products)
                    if all_featured and len(products) > 0:
                        self.log_test("Featured Products", True, f"Retrieved {len(products)} featured products")
                        return True, products
                    elif len(products) == 0:
                        self.log_test("Featured Products", False, "No featured products found")
                        return False, []
                    else:
                        non_featured = [p.get('name') for p in products if not p.get('featured', False)]
                        self.log_test("Featured Products", False, f"Non-featured products in results: {non_featured}")
                        return False, products
                else:
                    self.log_test("Featured Products", False, "Invalid response format", products)
                    return False, []
            else:
                self.log_test("Featured Products", False, f"HTTP {response.status_code}", response.text)
                return False, []
        except Exception as e:
            self.log_test("Featured Products", False, f"Connection error: {str(e)}")
            return False, []
    
    def test_product_detail(self, products: List[Dict]):
        """Test individual product detail endpoint"""
        if not products:
            self.log_test("Product Detail", False, "No products available to test detail endpoint")
            return
        
        # Test with first product
        test_product = products[0]
        product_id = test_product.get('id')
        
        try:
            response = self.session.get(f"{self.base_url}/products/{product_id}")
            if response.status_code == 200:
                product = response.json()
                if product.get('id') == product_id:
                    self.log_test("Product Detail", True, f"Retrieved product details for '{product.get('name')}'")
                else:
                    self.log_test("Product Detail", False, "Product ID mismatch", product)
            else:
                self.log_test("Product Detail", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Product Detail", False, f"Connection error: {str(e)}")
        
        # Test with invalid product ID
        try:
            response = self.session.get(f"{self.base_url}/products/invalid-id-12345")
            if response.status_code == 404:
                self.log_test("Product Detail 404", True, "Correctly returns 404 for invalid product ID")
            else:
                self.log_test("Product Detail 404", False, f"Expected 404, got {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Product Detail 404", False, f"Connection error: {str(e)}")
    
    def test_categories_endpoint(self):
        """Test categories endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/categories")
            if response.status_code == 200:
                categories = response.json()
                if isinstance(categories, list) and len(categories) > 0:
                    # Verify category structure
                    sample_category = categories[0]
                    if 'value' in sample_category and 'label' in sample_category:
                        expected_categories = ["crystals", "spiritual_jewelry", "amulets", "talismans", "protection_charms", "healing_stones"]
                        category_values = [cat.get('value') for cat in categories]
                        
                        if all(cat in category_values for cat in expected_categories):
                            self.log_test("Categories Endpoint", True, f"Retrieved {len(categories)} categories with correct structure")
                        else:
                            missing = [cat for cat in expected_categories if cat not in category_values]
                            self.log_test("Categories Endpoint", False, f"Missing categories: {missing}", categories)
                    else:
                        self.log_test("Categories Endpoint", False, "Invalid category structure", sample_category)
                else:
                    self.log_test("Categories Endpoint", False, "No categories found or invalid format", categories)
            else:
                self.log_test("Categories Endpoint", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Categories Endpoint", False, f"Connection error: {str(e)}")
    
    def test_sample_data_content(self, products: List[Dict]):
        """Test that sample lucky charm data is properly loaded"""
        if not products:
            self.log_test("Sample Data Content", False, "No products to verify sample data")
            return
        
        # Expected sample products (partial names to match)
        expected_products = [
            "Amethyst Crystal Cluster",
            "Sacred Geometry Crystal Grid", 
            "Rose Quartz Heart Stone",
            "Spiritual Protection Necklace",
            "Ocean Blessing Jewelry Set",
            "Golden Harmony Necklace"
        ]
        
        product_names = [p.get('name', '') for p in products]
        found_products = []
        
        for expected in expected_products:
            if any(expected in name for name in product_names):
                found_products.append(expected)
        
        if len(found_products) >= 4:  # Allow some flexibility
            self.log_test("Sample Data Content", True, f"Found {len(found_products)}/6 expected sample products")
            
            # Verify spiritual benefits are present
            products_with_benefits = [p for p in products if p.get('spiritual_benefits') and len(p.get('spiritual_benefits', [])) > 0]
            if len(products_with_benefits) > 0:
                self.log_test("Spiritual Benefits", True, f"{len(products_with_benefits)} products have spiritual benefits")
            else:
                self.log_test("Spiritual Benefits", False, "No products have spiritual benefits data")
                
            # Verify materials are present
            products_with_materials = [p for p in products if p.get('materials') and len(p.get('materials', [])) > 0]
            if len(products_with_materials) > 0:
                self.log_test("Materials Data", True, f"{len(products_with_materials)} products have materials data")
            else:
                self.log_test("Materials Data", False, "No products have materials data")
        else:
            self.log_test("Sample Data Content", False, f"Only found {len(found_products)}/6 expected sample products", found_products)
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print("=" * 60)
        print("LUCKY CHARM STORE BACKEND API TESTING")
        print("=" * 60)
        
        # Test basic connectivity
        if not self.test_root_endpoint():
            print("\n❌ CRITICAL: Cannot connect to backend API. Stopping tests.")
            return False
        
        print("\n" + "-" * 40)
        print("TESTING PRODUCT ENDPOINTS")
        print("-" * 40)
        
        # Test products endpoint and get sample data
        success, products = self.test_get_products()
        if not success:
            print("\n❌ CRITICAL: Cannot retrieve products. Stopping product tests.")
            return False
        
        # Test sample data content
        self.test_sample_data_content(products)
        
        # Test product detail endpoint
        self.test_product_detail(products)
        
        # Test categories endpoint
        self.test_categories_endpoint()
        
        # Test featured products
        self.test_featured_products()
        
        print("\n" + "-" * 40)
        print("TESTING SEARCH AND FILTERING")
        print("-" * 40)
        
        # Test search functionality
        self.test_product_search()
        
        # Test category filtering
        self.test_category_filtering()
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Tests Passed: {passed}/{total}")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Backend API is working correctly.")
            return True
        else:
            failed_tests = [result for result in self.test_results if not result['success']]
            print(f"\n❌ {len(failed_tests)} TESTS FAILED:")
            for test in failed_tests:
                print(f"   - {test['test']}: {test['message']}")
            return False

if __name__ == "__main__":
    tester = LuckyCharmAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)