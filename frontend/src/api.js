const BASE = "http://localhost:5000";

async function handleResponse(res) {
  const contentType = res.headers.get("content-type");
  let data = null;
  if (contentType && contentType.includes("application/json")) {
    data = await res.json();
  } else {
    data = await res.text();
  }
  if (!res.ok) {
    const err = (data && data.error) || data || res.statusText;
    throw new Error(err);
  }
  return data;
}

export async function fetchCategories() {
  const res = await fetch(`${BASE}/categories`);
  return handleResponse(res);
}

export async function fetchProducts(categoryId = null) {
  const url = new URL(`${BASE}/products`);
  if (categoryId) url.searchParams.append("categoryId", categoryId);
  const res = await fetch(url.toString());
  return handleResponse(res);
}

export async function fetchProductById(id) {
  const res = await fetch(`${BASE}/products/${id}`);
  return handleResponse(res);
}

export async function addToCart({ productId, quantity, userId = 1 }) {
  const res = await fetch(`${BASE}/cart/add`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ productId, quantity, userId })
  });
  return handleResponse(res);
}

export async function getCart(userId = 1) {
  const url = new URL(`${BASE}/cart`);
  // url.searchParams.append("userId", userId);
  const res = await fetch(url.toString());
  return handleResponse(res);
}

export async function setCartQuantity({ productId, quantity, userId = 1 }) {
  const res = await fetch(`${BASE}/cart/set-quantity`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ productId, quantity, userId })
  });
  return handleResponse(res);
}
