import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Header Component
const Header = ({ currentPage, setCurrentPage, searchTerm, setSearchTerm }) => {
  return (
    <header className="mystical-header">
      <div className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <div 
            className="logo-section cursor-pointer"
            onClick={() => setCurrentPage('home')}
          >
            <h1 className="text-3xl font-bold text-white">✨ MysticCharms</h1>
            <p className="text-purple-200 text-sm">Spiritual Treasures & Lucky Charms</p>
          </div>
          
          <div className="nav-links">
            <button 
              onClick={() => setCurrentPage('home')}
              className={`nav-button ${currentPage === 'home' ? 'active' : ''}`}
            >
              Home
            </button>
            <button 
              onClick={() => setCurrentPage('catalog')}
              className={`nav-button ${currentPage === 'catalog' ? 'active' : ''}`}
            >
              All Products
            </button>
            <button 
              onClick={() => setCurrentPage('categories')}
              className={`nav-button ${currentPage === 'categories' ? 'active' : ''}`}
            >
              Categories
            </button>
          </div>
          
          <div className="search-section">
            <div className="relative">
              <input
                type="text"
                placeholder="Search mystical items..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
              <span className="search-icon">🔮</span>
            </div>
          </div>
        </nav>
      </div>
    </header>
  );
};

// Product Card Component
const ProductCard = ({ product, onClick }) => {
  return (
    <div className="product-card" onClick={() => onClick(product)}>
      <div className="product-image-container">
        <img src={product.image_url} alt={product.name} className="product-image" />
        {product.featured && <span className="featured-badge">✨ Featured</span>}
      </div>
      <div className="product-content">
        <h3 className="product-name">{product.name}</h3>
        <p className="product-category">{product.category.replace('_', ' ')}</p>
        <p className="product-description">{product.description.substring(0, 100)}...</p>
        <div className="product-benefits">
          {product.spiritual_benefits.slice(0, 2).map((benefit, index) => (
            <span key={index} className="benefit-tag">{benefit}</span>
          ))}
        </div>
        <div className="product-footer">
          <span className="product-price">${product.price}</span>
          <button className="view-details-btn">View Details</button>
        </div>
      </div>
    </div>
  );
};

// Home Page Component
const HomePage = ({ products, setSelectedProduct }) => {
  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="container mx-auto px-4 py-16 text-center">
          <h1 className="hero-title">
            Discover Your Perfect Lucky Charm
          </h1>
          <p className="hero-subtitle">
            Handpicked spiritual treasures and mystical artifacts to bring positive energy into your life
          </p>
          <div className="hero-features">
            <div className="feature">
              <span className="feature-icon">🔮</span>
              <span>Authentic Crystals</span>
            </div>
            <div className="feature">
              <span className="feature-icon">✨</span>
              <span>Spiritual Jewelry</span>
            </div>
            <div className="feature">
              <span className="feature-icon">🧿</span>
              <span>Protection Charms</span>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="featured-section">
        <div className="container mx-auto px-4 py-12">
          <h2 className="section-title">✨ Featured Lucky Charms</h2>
          <div className="products-grid">
            {products.filter(p => p.featured).map(product => (
              <ProductCard 
                key={product.id} 
                product={product} 
                onClick={setSelectedProduct}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Categories Preview */}
      <section className="categories-preview">
        <div className="container mx-auto px-4 py-12">
          <h2 className="section-title">Shop by Category</h2>
          <div className="categories-grid">
            <div className="category-card crystals">
              <h3>🔮 Crystals & Gems</h3>
              <p>Powerful healing stones and crystal formations</p>
            </div>
            <div className="category-card jewelry">
              <h3>✨ Spiritual Jewelry</h3>
              <p>Beautiful jewelry with mystical properties</p>
            </div>
            <div className="category-card protection">
              <h3>🧿 Protection Charms</h3>
              <p>Amulets and talismans for spiritual protection</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

// Product Catalog Component
const ProductCatalog = ({ products, searchTerm, setSelectedProduct }) => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  
  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const categories = [
    { value: 'all', label: 'All Products' },
    { value: 'crystals', label: 'Crystals' },
    { value: 'spiritual_jewelry', label: 'Spiritual Jewelry' },
    { value: 'amulets', label: 'Amulets' },
    { value: 'talismans', label: 'Talismans' },
    { value: 'protection_charms', label: 'Protection Charms' },
    { value: 'healing_stones', label: 'Healing Stones' }
  ];

  return (
    <div className="catalog-page">
      <div className="container mx-auto px-4 py-8">
        <div className="catalog-header">
          <h1 className="page-title">🔮 Product Catalog</h1>
          <p className="page-subtitle">Explore our complete collection of mystical treasures</p>
        </div>

        {/* Category Filter */}
        <div className="filter-section">
          <h3 className="filter-title">Filter by Category:</h3>
          <div className="category-filters">
            {categories.map(category => (
              <button
                key={category.value}
                onClick={() => setSelectedCategory(category.value)}
                className={`filter-btn ${selectedCategory === category.value ? 'active' : ''}`}
              >
                {category.label}
              </button>
            ))}
          </div>
        </div>

        {/* Products Grid */}
        <div className="products-section">
          <div className="products-count">
            Showing {filteredProducts.length} products
          </div>
          <div className="products-grid">
            {filteredProducts.map(product => (
              <ProductCard 
                key={product.id} 
                product={product} 
                onClick={setSelectedProduct}
              />
            ))}
          </div>
          
          {filteredProducts.length === 0 && (
            <div className="no-products">
              <p>No products found matching your criteria.</p>
              <p>Try adjusting your search or category filter.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Product Detail Modal
const ProductDetail = ({ product, onClose }) => {
  if (!product) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="product-modal" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>×</button>
        
        <div className="modal-content">
          <div className="modal-image-section">
            <img src={product.image_url} alt={product.name} className="modal-image" />
          </div>
          
          <div className="modal-details">
            <h2 className="modal-title">{product.name}</h2>
            <p className="modal-category">{product.category.replace('_', ' ')}</p>
            <p className="modal-price">${product.price}</p>
            
            <div className="modal-description">
              <h4>Description</h4>
              <p>{product.description}</p>
            </div>
            
            {product.spiritual_benefits.length > 0 && (
              <div className="modal-benefits">
                <h4>Spiritual Benefits</h4>
                <div className="benefits-list">
                  {product.spiritual_benefits.map((benefit, index) => (
                    <span key={index} className="benefit-tag">{benefit}</span>
                  ))}
                </div>
              </div>
            )}
            
            {product.materials.length > 0 && (
              <div className="modal-materials">
                <h4>Materials</h4>
                <p>{product.materials.join(', ')}</p>
              </div>
            )}
            
            {product.origin && (
              <div className="modal-origin">
                <h4>Origin</h4>
                <p>{product.origin}</p>
              </div>
            )}
            
            <div className="modal-actions">
              <button className="add-to-wishlist-btn">💜 Add to Wishlist</button>
              <button className="contact-seller-btn">📧 Contact for Purchase</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Main App Component
function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/products`);
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-content">
          <div className="loading-spinner">🔮</div>
          <p>Loading mystical treasures...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <Header 
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
      />
      
      <main className="main-content">
        {currentPage === 'home' && (
          <HomePage 
            products={products}
            setSelectedProduct={setSelectedProduct}
          />
        )}
        
        {(currentPage === 'catalog' || currentPage === 'categories') && (
          <ProductCatalog 
            products={products}
            searchTerm={searchTerm}
            setSelectedProduct={setSelectedProduct}
          />
        )}
      </main>
      
      {selectedProduct && (
        <ProductDetail 
          product={selectedProduct}
          onClose={() => setSelectedProduct(null)}
        />
      )}
    </div>
  );
}

export default App;