import React from "react";

function Node({ node, level = 0, onSelect }) {
  const hasChildren = node.children && node.children.length > 0;
  return (
    <div style={{ marginLeft: level * 10 }}>
      <div className="category-item" onClick={() => onSelect(node)}>
        <span style={{ marginRight: 8 }}>{hasChildren ? "▸" : "•"}</span>
        <strong>{node.name}</strong>
      </div>
      {hasChildren && (
        <div>
          {node.children.map((c) => (
            <Node key={c.id} node={c} level={level + 1} onSelect={onSelect} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function CategoryTree({ tree = [], onSelect = () => {} }) {
  if (!tree || tree.length === 0) {
    return <div className="card">No categories found</div>;
  }
  return (
    <div className="card">
      <h4>Categories</h4>
      <div>
        {tree.map((root) => (
          <Node key={root.id} node={root} onSelect={onSelect} />
        ))}
      </div>
    </div>
  );
}
