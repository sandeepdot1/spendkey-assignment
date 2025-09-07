import React, { useState } from "react";

export default function ProductCard({ product, onAdd }) {
  const [qty, setQty] = useState(1);
  const disabled = product.availability_qty <= 0;

  return (
    <div className="card product-card">
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <div><strong>{product.name}</strong></div>
        <div className="small">₹{Number(product.price).toFixed(2)}</div>
      </div>

      <div className="small">Available: {product.availabilityQty}</div>

      <div style={{ marginTop: "auto" }}>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <input
            className="input"
            type="number"
            min="1"
            value={qty}
            onChange={(e) => setQty(Math.max(1, parseInt(e.target.value || 1)))}
            style={{ width: 80 }}
          />
          <button className="btn btn-primary" disabled={disabled} onClick={() => onAdd(product.id, qty)}>
            Add to Cart
          </button>
        </div>
        {disabled && <div style={{ color: "crimson", marginTop: 6 }}>Out of stock</div>}
      </div>
    </div>
  );
}
