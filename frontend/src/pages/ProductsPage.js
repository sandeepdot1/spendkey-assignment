// frontend/src/pages/ProductsPage.js
import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import ProductCard from "../components/ProductCard";
import { fetchProducts, addToCart, fetchCategories } from "../api";

export default function ProductsPage() {
  const [searchParams] = useSearchParams();
  const categoryId = searchParams.get("categoryId");
  const [products, setProducts] = useState([]);
  const [categoryName, setCategoryName] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      // fetch products
      const data = await fetchProducts(categoryId);
      // Only show if availabilityQty > 0
      const visible = data.filter((p) => p.availabilityQty > 0);
      setProducts(visible);

      // fetch categories to resolve category name
      if (categoryId) {
        const cats = await fetchCategories();
        const findCat = (list, id) => {
          for (let c of list) {
            if (c.id === parseInt(id)) return c;
            if (c.children) {
              const found = findCat(c.children, id);
              if (found) return found;
            }
          }
          return null;
        };
        const cat = findCat(cats, categoryId);
        setCategoryName(cat ? cat.name : "");
      } else {
        setCategoryName("");
      }
    } catch (e) {
      setError(e.message || "Failed to fetch products");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line
  }, [categoryId]);

  const handleAdd = async (productId, qty) => {
    setMessage(null);
    setError(null);
    try {
      await addToCart({ productId, quantity: qty, userId: 0 }); // demo userId=1
      setMessage("Added to cart");
      // refresh products to show updated availability (simple approach)
      await load();
    } catch (e) {
      setError(e.message || "Failed to add to cart");
    }
  };

  return (
    <div>
      <div className="card">
        <h3>
          Products {categoryName ? `(${categoryName})` : ""}
        </h3>
      </div>

      {loading && <div className="card">Loading...</div>}
      {error && <div className="card" style={{ color: "crimson" }}>{error}</div>}
      {message && <div className="card" style={{ color: "green" }}>{message}</div>}

      <div style={{ marginTop: 12 }}>
        <div className="product-grid">
          {!loading && products.length === 0 && (
            <div className="card">No products available</div>
          )}
          {products.map((p) => (
            <ProductCard key={p.id} product={p} onAdd={handleAdd} />
          ))}
        </div>
      </div>
    </div>
  );
}
