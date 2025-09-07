import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import CategoryTree from "../components/CategoryTree";
import { fetchCategories } from "../api";

export default function CategoriesPage() {
  const [tree, setTree] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    setLoading(true);
    fetchCategories()
      .then((data) => {
        // backend returns nested tree; ensure children property exists
        setTree(data);
      })
      .catch((err) => setError(err.message || "Failed to load"))
      .finally(() => setLoading(false));
  }, []);

  const onSelect = (node) => {
    // navigate to products page and pass categoryId param
    navigate(`/products?categoryId=${node.id}`);
  };

  return (
    <div className="layout">
      <div>
        <div className="card">
          <h3>Browse Categories</h3>
          {loading && <div>Loading...</div>}
          {error && <div style={{ color: "crimson" }}>{error}</div>}
        </div>
        <CategoryTree tree={tree} onSelect={onSelect} />
      </div>

      <div>
        <div className="card">
          <h3>How to use</h3>
          <p className="small">Click a category to view products in that category (includes subcategories).</p>
        </div>
      </div>
    </div>
  );
}
