import React, { useEffect, useState } from "react";
import { getCart, setCartQuantity } from "../api";

export default function CartPage() {
  const [cart, setCart] = useState({ items: [], total: 0, userId: 0 });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [editing, setEditing] = useState({}); // productId -> qty

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getCart();
      setCart(data);
      const ed = {};
      (data.items || []).forEach((it) => (ed[it.productId] = it.quantity));
      setEditing(ed);
    } catch (e) {
      setError(e.message || "Failed to load cart");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const updateQty = async (productId, qty) => {
    setError(null);
    try {
      await setCartQuantity({ productId, quantity: qty, userId: cart.userId });
      await load();
    } catch (e) {
      setError(e.message || "Failed to update cart");
    }
  };

  return (
    <div>
      <div className="card">
        <h3>Your Cart</h3>
      </div>

      {loading && <div className="card">Loading...</div>}
      {error && <div className="card" style={{ color: "crimson" }}>{error}</div>}

      <div style={{ marginTop: 12 }}>
        <div className="card">
          {cart.items.length === 0 ? (
            <div>No items in cart</div>
          ) : (
            <>
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr>
                    <th align="left">Product</th>
                    <th align="left">Unit Price</th>
                    <th align="left">Quantity</th>
                    <th align="left">Line Total</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {cart.items.map((it) => (
                    <tr key={it.productId} style={{ borderTop: "1px solid #eee" }}>
                      <td>{it.name}</td>
                      <td>₹{Number(it.unitPrice).toFixed(2)}</td>
                      <td>
                        <input
                          className="input"
                          type="number"
                          min="0"
                          value={editing[it.productId]}
                          onChange={(e) =>
                            setEditing((prev) => ({ ...prev, [it.productId]: Math.max(0, parseInt(e.target.value || 0)) }))
                          }
                          style={{ width: 80 }}
                        />
                      </td>
                      <td>₹{Number(it.lineTotal).toFixed(2)}</td>
                      <td className="row">
                        <button
                          className="btn btn-primary"
                          onClick={() => updateQty(it.productId, Number(editing[it.productId] || 0))}
                        >
                          Update
                        </button>
                        <button className="btn btn-secondary" onClick={() => updateQty(it.productId, 0)}>
                          Remove
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div style={{ marginTop: 12, textAlign: "right" }}>
                <strong>Total: ₹{Number(cart.total).toFixed(2)}</strong>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
