"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const [cosmetics, setCosmetics] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`http://localhost:8000/cosmetics?page=${page}&page_size=5`)
      .then((res) => res.json())
      .then((data) => {
        setCosmetics(data.items);
        setTotalPages(data.total_pages);
        setLoading(false);
      });
  }, [page]);

  return (
    <main style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.heading}>💄 Cosmetics Catalog</h1>

        <section style={styles.listSection}>
          {loading ? (
            <p style={styles.loadingText}>Loading...</p>
          ) : (
            <ul style={styles.list}>
              {cosmetics.map((item) => (
                <li key={item.id} style={styles.listItem}>
                  <span style={styles.itemName}>{item.name}</span>
                  <span style={styles.itemBrand}>{item.brand}</span>
                  <span style={styles.itemPrice}>Ksh{item.price}</span>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section style={styles.pagination}>
          <button
            onClick={() => setPage(page - 1)}
            disabled={page <= 1}
            style={{ ...styles.navButton, ...(page <= 1 ? styles.navButtonDisabled : {}) }}
          >
            ← Previous
          </button>
          <span style={styles.pageIndicator}>Page {page} of {totalPages}</span>
          <button
            onClick={() => setPage(page + 1)}
            disabled={page >= totalPages}
            style={{ ...styles.navButtonPrimary, ...(page >= totalPages ? styles.navButtonDisabled : {}) }}
          >
            Next →
          </button>
        </section>
      </div>
    </main>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    backgroundColor: "#fff0f5",
    backgroundImage:
      "radial-gradient(circle at 20% 20%, #ffd6e8 2px, transparent 2px), radial-gradient(circle at 60% 70%, #ffc2dd 2px, transparent 2px), radial-gradient(circle at 85% 30%, #ffd6e8 1.5px, transparent 1.5px)",
    backgroundSize: "40px 40px, 60px 60px, 30px 30px",
    padding: "3rem 1rem",
    display: "flex",
    justifyContent: "center",
    fontFamily: "'Segoe UI', sans-serif",
  },
  card: {
    background: "#fff",
    borderRadius: "20px",
    padding: "2.5rem",
    maxWidth: "600px",
    width: "100%",
    boxShadow: "0 10px 30px rgba(255, 105, 180, 0.15)",
    border: "2px dashed #ffb3d1",
  },
  heading: {
    textAlign: "center",
    color: "#d6336c",
    marginBottom: "1.5rem",
  },
  listSection: {
    borderBottom: "2px dashed #ffd6e8",
    paddingBottom: "1.5rem",
    marginBottom: "1.5rem",
  },
  loadingText: {
    textAlign: "center",
    color: "#d6336c",
  },
  list: {
    listStyle: "none",
    padding: 0,
    margin: 0,
  },
  listItem: {
    display: "flex",
    justifyContent: "space-between",
    padding: "0.75rem 1rem",
    marginBottom: "0.5rem",
    background: "#fff5f9",
    borderRadius: "10px",
  },
  itemName: { fontWeight: "bold", color: "#7a1f4a" },
  itemBrand: { color: "#b25b84" },
  itemPrice: { fontWeight: "bold", color: "#d6336c" },
  pagination: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
  },
  pageIndicator: {
    color: "#7a1f4a",
    fontWeight: "500",
  },
  navButton: {
    background: "#fff",
    color: "#d6336c",
    border: "2px solid #d6336c",
    borderRadius: "999px",
    padding: "0.5rem 1.2rem",
    cursor: "pointer",
    fontWeight: "bold",
  },
  navButtonPrimary: {
    background: "linear-gradient(135deg, #ff6fa5, #ff3d81)",
    color: "#fff",
    border: "none",
    borderRadius: "999px",
    padding: "0.6rem 1.4rem",
    cursor: "pointer",
    fontWeight: "bold",
    boxShadow: "0 4px 12px rgba(255, 61, 129, 0.4)",
  },
  navButtonDisabled: {
    opacity: 0.4,
    cursor: "not-allowed",
    boxShadow: "none",
  },
};