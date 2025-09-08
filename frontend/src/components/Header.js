import React from "react";
import { Link } from "react-router-dom";

export default function Header() {
  return (
    <header className="header">
      <div className="container" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <Link to="/categories" style={{ color: "white", textDecoration: "none", fontWeight: "700" }}>
            E-Commerce
          </Link>
        </div>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <Link to="/cart" style={{ color: "white", textDecoration: "none" }}>Cart</Link>
          {/* <Link to="/products" style={{ color: "white", textDecoration: "none" }}>Products</Link> */}
        </div>
      </div>
    </header>
  );
}
