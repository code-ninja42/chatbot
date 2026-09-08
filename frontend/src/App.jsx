// import { useEffect, useState } from "react";

// const API = "http://127.0.0.1:8000";

// function App() {
//   const [page, setPage] = useState("chat");

//   // Chat
//   const [message, setMessage] = useState("");
//   const [messages, setMessages] = useState([
//     {
//       sender: "bot",
//       text: "Hello! 👋 I'm your store assistant. Ask me about products, prices, stock, or orders."
//     }
//   ]);

//   // Products
//   const [products, setProducts] = useState([]);

//   // Orders
//   const [orders, setOrders] = useState([]);

//   // Product form
//   const [product, setProduct] = useState({
//     name: "",
//     description: "",
//     category: "",
//     price: "",
//     stock: "",
//     availability: true
//   });

//   // Order form
//   const [order, setOrder] = useState({
//     customer_name: "",
//     customer_email: "",
//     product_id: "",
//     quantity: 1
//   });

//   // Load products
//   const loadProducts = async () => {
//     try {
//       const response = await fetch(`${API}/products`);
//       const data = await response.json();
//       setProducts(data.products);
//     } catch (error) {
//       console.log(error);
//     }
//   };

//   // Load orders
//   const loadOrders = async () => {
//     try {
//       const response = await fetch(`${API}/orders`);
//       const data = await response.json();
//       setOrders(data.orders);
//     } catch (error) {
//       console.log(error);
//     }
//   };

//   useEffect(() => {
//     loadProducts();
//     loadOrders();
//   }, []);

//   // =========================
//   // CHAT
//   // =========================

//   const sendMessage = async () => {
//     if (!message.trim()) return;

//     const userMessage = message;

//     setMessages((oldMessages) => [
//       ...oldMessages,
//       {
//         sender: "user",
//         text: userMessage
//       }
//     ]);

//     setMessage("");

//     try {
//       const response = await fetch(`${API}/chat`, {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json"
//         },
//         body: JSON.stringify({
//           question: userMessage
//         })
//       });

//       const data = await response.json();

//       setMessages((oldMessages) => [
//         ...oldMessages,
//         {
//           sender: "bot",
//           text: data.answer
//         }
//       ]);
//     } catch (error) {
//       setMessages((oldMessages) => [
//         ...oldMessages,
//         {
//           sender: "bot",
//           text: "Sorry, I could not connect to the chatbot server."
//         }
//       ]);
//     }
//   };

//   // =========================
//   // ADD PRODUCT
//   // =========================

//   const addProduct = async (e) => {
//     e.preventDefault();

//     try {
//       const response = await fetch(`${API}/products`, {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json"
//         },
//         body: JSON.stringify({
//           name: product.name,
//           description: product.description,
//           category: product.category,
//           price: Number(product.price),
//           stock: Number(product.stock),
//           availability: product.availability
//         })
//       });

//       const data = await response.json();

//       if (!response.ok) {
//         alert(data.detail || "Failed to add product");
//         return;
//       }

//       alert("Product added successfully!");

//       setProduct({
//         name: "",
//         description: "",
//         category: "",
//         price: "",
//         stock: "",
//         availability: true
//       });

//       loadProducts();
//     } catch (error) {
//       alert("Could not connect to backend.");
//     }
//   };

//   // =========================
//   // PLACE ORDER
//   // =========================

//   const placeOrder = async (e) => {
//     e.preventDefault();

//     try {
//       const response = await fetch(`${API}/orders`, {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json"
//         },
//         body: JSON.stringify({
//           customer_name: order.customer_name,
//           customer_email: order.customer_email,
//           product_id: Number(order.product_id),
//           quantity: Number(order.quantity)
//         })
//       });

//       const data = await response.json();

//       if (!response.ok) {
//         alert(data.detail || "Failed to place order");
//         return;
//       }

//       alert(`Order placed successfully! Order ID: ${data.order_id}`);

//       setOrder({
//         customer_name: "",
//         customer_email: "",
//         product_id: "",
//         quantity: 1
//       });

//       loadProducts();
//       loadOrders();
//     } catch (error) {
//       alert("Could not connect to backend.");
//     }
//   };

//   return (
//     <div className="app">

//       {/* ================= HEADER ================= */}

//       <header className="top-header">

//         <div>
//           <h1>🛍️ Store Assistant</h1>
//           <p>AI Store Management System</p>
//         </div>

//         <nav>
//           <button
//             className={page === "chat" ? "active" : ""}
//             onClick={() => setPage("chat")}
//           >
//             💬 Chat
//           </button>

//           <button
//             className={page === "products" ? "active" : ""}
//             onClick={() => setPage("products")}
//           >
//             📦 Products
//           </button>

//           <button
//             className={page === "order" ? "active" : ""}
//             onClick={() => setPage("order")}
//           >
//             🛒 Place Order
//           </button>

//           <button
//             className={page === "admin" ? "active" : ""}
//             onClick={() => setPage("admin")}
//           >
//             ⚙️ Admin
//           </button>
//         </nav>

//       </header>


//       {/* ================= CHAT ================= */}

//       {page === "chat" && (

//         <div className="chat-container">

//           <div className="messages">

//             {messages.map((msg, index) => (

//               <div
//                 key={index}
//                 className={
//                   msg.sender === "user"
//                     ? "message user-message"
//                     : "message bot-message"
//                 }
//               >
//                 {msg.text}
//               </div>

//             ))}

//           </div>

//           <div className="input-area">

//             <input
//               type="text"
//               placeholder="Ask about products, prices, stock..."
//               value={message}
//               onChange={(e) => setMessage(e.target.value)}
//               onKeyDown={(e) => {
//                 if (e.key === "Enter") {
//                   sendMessage();
//                 }
//               }}
//             />

//             <button onClick={sendMessage}>
//               Send
//             </button>

//           </div>

//         </div>

//       )}


//       {/* ================= PRODUCTS ================= */}

//       {page === "products" && (

//         <div className="page">

//           <h2>📦 Products</h2>

//           <div className="product-grid">

//             {products.map((item) => (

//               <div className="product-card" key={item.id}>

//                 <h3>{item.name}</h3>

//                 <p>{item.description}</p>

//                 <p>
//                   <strong>Category:</strong> {item.category}
//                 </p>

//                 <p>
//                   <strong>Price:</strong> ₹{item.price}
//                 </p>

//                 <p>
//                   <strong>Stock:</strong> {item.stock}
//                 </p>

//                 <p>
//                   <strong>Status:</strong>{" "}
//                   {item.availability ? "Available" : "Unavailable"}
//                 </p>

//               </div>

//             ))}

//           </div>

//         </div>

//       )}


//       {/* ================= PLACE ORDER ================= */}

//       {page === "order" && (

//         <div className="page">

//           <h2>🛒 Place Order</h2>

//           <form className="form" onSubmit={placeOrder}>

//             <input
//               type="text"
//               placeholder="Customer name"
//               value={order.customer_name}
//               onChange={(e) =>
//                 setOrder({
//                   ...order,
//                   customer_name: e.target.value
//                 })
//               }
//               required
//             />

//             <input
//               type="email"
//               placeholder="Customer email"
//               value={order.customer_email}
//               onChange={(e) =>
//                 setOrder({
//                   ...order,
//                   customer_email: e.target.value
//                 })
//               }
//             />

//             <select
//               value={order.product_id}
//               onChange={(e) =>
//                 setOrder({
//                   ...order,
//                   product_id: e.target.value
//                 })
//               }
//               required
//             >

//               <option value="">
//                 Select product
//               </option>

//               {products.map((item) => (

//                 <option key={item.id} value={item.id}>
//                   {item.name} - ₹{item.price}
//                 </option>

//               ))}

//             </select>

//             <input
//               type="number"
//               min="1"
//               placeholder="Quantity"
//               value={order.quantity}
//               onChange={(e) =>
//                 setOrder({
//                   ...order,
//                   quantity: e.target.value
//                 })
//               }
//               required
//             />

//             <button type="submit">
//               Place Order
//             </button>

//           </form>

//         </div>

//       )}


//       {/* ================= ADMIN ================= */}

//       {page === "admin" && (

//         <div className="page">

//           <h2>⚙️ Admin Panel</h2>

//           <div className="admin-buttons">

//             <button
//               onClick={() => setPage("add-product")}
//             >
//               ➕ Add Product
//             </button>

//             <button
//               onClick={() => {
//                 loadOrders();
//                 setPage("orders");
//               }}
//             >
//               📋 View Orders
//             </button>

//           </div>

//         </div>

//       )}


//       {/* ================= ADD PRODUCT ================= */}

//       {page === "add-product" && (

//         <div className="page">

//           <h2>➕ Add Product</h2>

//           <form className="form" onSubmit={addProduct}>

//             <input
//               type="text"
//               placeholder="Product name"
//               value={product.name}
//               onChange={(e) =>
//                 setProduct({
//                   ...product,
//                   name: e.target.value
//                 })
//               }
//               required
//             />

//             <input
//               type="text"
//               placeholder="Description"
//               value={product.description}
//               onChange={(e) =>
//                 setProduct({
//                   ...product,
//                   description: e.target.value
//                 })
//               }
//             />

//             <input
//               type="text"
//               placeholder="Category"
//               value={product.category}
//               onChange={(e) =>
//                 setProduct({
//                   ...product,
//                   category: e.target.value
//                 })
//               }
//             />

//             <input
//               type="number"
//               placeholder="Price"
//               value={product.price}
//               onChange={(e) =>
//                 setProduct({
//                   ...product,
//                   price: e.target.value
//                 })
//               }
//               required
//             />

//             <input
//               type="number"
//               placeholder="Stock"
//               value={product.stock}
//               onChange={(e) =>
//                 setProduct({
//                   ...product,
//                   stock: e.target.value
//                 })
//               }
//               required
//             />

//             <label>
//               <input
//                 type="checkbox"
//                 checked={product.availability}
//                 onChange={(e) =>
//                   setProduct({
//                     ...product,
//                     availability: e.target.checked
//                   })
//                 }
//               />

//               Available
//             </label>

//             <button type="submit">
//               Add Product
//             </button>

//           </form>

//         </div>

//       )}


//       {/* ================= ORDERS ================= */}

//       {page === "orders" && (

//         <div className="page">

//           <h2>📋 Orders</h2>

//           <button
//             className="refresh"
//             onClick={loadOrders}
//           >
//             🔄 Refresh Orders
//           </button>

//           <div className="orders-container">

//             {orders.length === 0 ? (

//               <p>No orders found.</p>

//             ) : (

//               <table>

//                 <thead>
//                   <tr>
//                     <th>ID</th>
//                     <th>Customer</th>
//                     <th>Product ID</th>
//                     <th>Quantity</th>
//                     <th>Total</th>
//                     <th>Status</th>
//                     <th>Tracking</th>
//                   </tr>
//                 </thead>

//                 <tbody>

//                   {orders.map((item) => (

//                     <tr key={item.id}>

//                       <td>{item.id}</td>

//                       <td>{item.customer_name}</td>

//                       <td>{item.product_id}</td>

//                       <td>{item.quantity}</td>

//                       <td>₹{item.total_amount}</td>

//                       <td>{item.status}</td>

//                       <td>
//                         {item.tracking_number || "-"}
//                       </td>

//                     </tr>

//                   ))}

//                 </tbody>

//               </table>

//             )}

//           </div>

//         </div>

//       )}

//     </div>
//   );
// }

// export default App;
import { useEffect, useState } from "react";

// ==========================================
// BACKEND API
// ==========================================

const API = "https://chatbot-project-pro5.onrender.com";

function App() {
  const [page, setPage] = useState("chat");

  // ==========================================
  // CHAT
  // ==========================================

  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! 👋 I'm your store assistant. Ask me about products, prices, stock, or orders."
    }
  ]);

  // ==========================================
  // PRODUCTS
  // ==========================================

  const [products, setProducts] = useState([]);

  // ==========================================
  // ORDERS
  // ==========================================

  const [orders, setOrders] = useState([]);

  // ==========================================
  // PRODUCT FORM
  // ==========================================

  const [product, setProduct] = useState({
    name: "",
    description: "",
    category: "",
    price: "",
    stock: "",
    availability: true
  });

  // ==========================================
  // ORDER FORM
  // ==========================================

  const [order, setOrder] = useState({
    customer_name: "",
    customer_email: "",
    product_id: "",
    quantity: 1
  });

  // ==========================================
  // LOAD PRODUCTS
  // ==========================================

  const loadProducts = async () => {
    try {
      const response = await fetch(`${API}/products`);

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to load products");
      }

      setProducts(data.products || []);
    } catch (error) {
      console.error("Products error:", error);
    }
  };

  // ==========================================
  // LOAD ORDERS
  // ==========================================

  const loadOrders = async () => {
    try {
      const response = await fetch(`${API}/orders`);

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to load orders");
      }

      setOrders(data.orders || []);
    } catch (error) {
      console.error("Orders error:", error);
    }
  };

  // ==========================================
  // LOAD DATA WHEN APP STARTS
  // ==========================================

  useEffect(() => {
    loadProducts();
    loadOrders();
  }, []);

  // ==========================================
  // CHAT
  // ==========================================

  const sendMessage = async () => {
    if (!message.trim()) {
      return;
    }

    const userMessage = message.trim();

    // Show user message immediately
    setMessages((oldMessages) => [
      ...oldMessages,
      {
        sender: "user",
        text: userMessage
      }
    ]);

    setMessage("");

    try {
      const response = await fetch(`${API}/chat`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          question: userMessage
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Chat request failed"
        );
      }

      setMessages((oldMessages) => [
        ...oldMessages,
        {
          sender: "bot",
          text: data.answer || "No response received."
        }
      ]);
    } catch (error) {
      console.error("Chat error:", error);

      setMessages((oldMessages) => [
        ...oldMessages,
        {
          sender: "bot",
          text: `Error: ${error.message}`
        }
      ]);
    }
  };

  // ==========================================
  // ADD PRODUCT
  // ==========================================

  const addProduct = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${API}/products`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          name: product.name,
          description: product.description,
          category: product.category,
          price: Number(product.price),
          stock: Number(product.stock),
          availability: product.availability
        })
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail || "Failed to add product");
        return;
      }

      alert("Product added successfully!");

      setProduct({
        name: "",
        description: "",
        category: "",
        price: "",
        stock: "",
        availability: true
      });

      await loadProducts();

      setPage("products");
    } catch (error) {
      console.error("Add product error:", error);

      alert(`Could not connect to backend: ${error.message}`);
    }
  };

  // ==========================================
  // PLACE ORDER
  // ==========================================

  const placeOrder = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${API}/orders`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          customer_name: order.customer_name,
          customer_email: order.customer_email,
          product_id: Number(order.product_id),
          quantity: Number(order.quantity)
        })
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail || "Failed to place order");
        return;
      }

      alert(
        `Order placed successfully! Order ID: ${data.order_id}`
      );

      setOrder({
        customer_name: "",
        customer_email: "",
        product_id: "",
        quantity: 1
      });

      await loadProducts();
      await loadOrders();

      setPage("orders");
    } catch (error) {
      console.error("Order error:", error);

      alert(`Could not connect to backend: ${error.message}`);
    }
  };

  // ==========================================
  // UI
  // ==========================================

  return (
    <div className="app">

      {/* ======================================
          HEADER
      ====================================== */}

      <header className="top-header">

        <div>
          <h1>🛍️ Store Assistant</h1>

          <p>
            AI Store Management System
          </p>
        </div>

        <nav>

          <button
            className={page === "chat" ? "active" : ""}
            onClick={() => setPage("chat")}
          >
            💬 Chat
          </button>

          <button
            className={page === "products" ? "active" : ""}
            onClick={() => setPage("products")}
          >
            📦 Products
          </button>

          <button
            className={page === "order" ? "active" : ""}
            onClick={() => setPage("order")}
          >
            🛒 Place Order
          </button>

          <button
            className={page === "admin" ? "active" : ""}
            onClick={() => setPage("admin")}
          >
            ⚙️ Admin
          </button>

        </nav>

      </header>

      {/* ======================================
          CHAT
      ====================================== */}

      {page === "chat" && (

        <div className="chat-container">

          <div className="messages">

            {messages.map((msg, index) => (

              <div
                key={index}
                className={
                  msg.sender === "user"
                    ? "message user-message"
                    : "message bot-message"
                }
              >
                {msg.text}
              </div>

            ))}

          </div>

          <div className="input-area">

            <input
              type="text"
              placeholder="Ask about products, prices, stock..."
              value={message}
              onChange={(e) =>
                setMessage(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
            />

            <button onClick={sendMessage}>
              Send
            </button>

          </div>

        </div>

      )}

      {/* ======================================
          PRODUCTS
      ====================================== */}

      {page === "products" && (

        <div className="page">

          <h2>📦 Products</h2>

          <div className="product-grid">

            {products.length === 0 ? (

              <p>No products found.</p>

            ) : (

              products.map((item) => (

                <div
                  className="product-card"
                  key={item.id}
                >

                  <h3>{item.name}</h3>

                  <p>
                    {item.description}
                  </p>

                  <p>
                    <strong>
                      Category:
                    </strong>{" "}
                    {item.category}
                  </p>

                  <p>
                    <strong>
                      Price:
                    </strong>{" "}
                    ₹{item.price}
                  </p>

                  <p>
                    <strong>
                      Stock:
                    </strong>{" "}
                    {item.stock}
                  </p>

                  <p>
                    <strong>
                      Status:
                    </strong>{" "}

                    {item.availability
                      ? "Available"
                      : "Unavailable"}
                  </p>

                </div>

              ))

            )}

          </div>

        </div>

      )}

      {/* ======================================
          PLACE ORDER
      ====================================== */}

      {page === "order" && (

        <div className="page">

          <h2>🛒 Place Order</h2>

          <form
            className="form"
            onSubmit={placeOrder}
          >

            <input
              type="text"
              placeholder="Customer name"
              value={order.customer_name}
              onChange={(e) =>
                setOrder({
                  ...order,
                  customer_name: e.target.value
                })
              }
              required
            />

            <input
              type="email"
              placeholder="Customer email"
              value={order.customer_email}
              onChange={(e) =>
                setOrder({
                  ...order,
                  customer_email: e.target.value
                })
              }
            />

            <select
              value={order.product_id}
              onChange={(e) =>
                setOrder({
                  ...order,
                  product_id: e.target.value
                })
              }
              required
            >

              <option value="">
                Select product
              </option>

              {products.map((item) => (

                <option
                  key={item.id}
                  value={item.id}
                >
                  {item.name} - ₹{item.price}
                </option>

              ))}

            </select>

            <input
              type="number"
              min="1"
              placeholder="Quantity"
              value={order.quantity}
              onChange={(e) =>
                setOrder({
                  ...order,
                  quantity: e.target.value
                })
              }
              required
            />

            <button type="submit">
              Place Order
            </button>

          </form>

        </div>

      )}

      {/* ======================================
          ADMIN
      ====================================== */}

      {page === "admin" && (

        <div className="page">

          <h2>⚙️ Admin Panel</h2>

          <div className="admin-buttons">

            <button
              onClick={() =>
                setPage("add-product")
              }
            >
              ➕ Add Product
            </button>

            <button
              onClick={async () => {
                await loadOrders();
                setPage("orders");
              }}
            >
              📋 View Orders
            </button>

          </div>

        </div>

      )}

      {/* ======================================
          ADD PRODUCT
      ====================================== */}

      {page === "add-product" && (

        <div className="page">

          <h2>➕ Add Product</h2>

          <form
            className="form"
            onSubmit={addProduct}
          >

            <input
              type="text"
              placeholder="Product name"
              value={product.name}
              onChange={(e) =>
                setProduct({
                  ...product,
                  name: e.target.value
                })
              }
              required
            />

            <input
              type="text"
              placeholder="Description"
              value={product.description}
              onChange={(e) =>
                setProduct({
                  ...product,
                  description: e.target.value
                })
              }
            />

            <input
              type="text"
              placeholder="Category"
              value={product.category}
              onChange={(e) =>
                setProduct({
                  ...product,
                  category: e.target.value
                })
              }
            />

            <input
              type="number"
              placeholder="Price"
              min="0"
              value={product.price}
              onChange={(e) =>
                setProduct({
                  ...product,
                  price: e.target.value
                })
              }
              required
            />

            <input
              type="number"
              placeholder="Stock"
              min="0"
              value={product.stock}
              onChange={(e) =>
                setProduct({
                  ...product,
                  stock: e.target.value
                })
              }
              required
            />

            <label>

              <input
                type="checkbox"
                checked={product.availability}
                onChange={(e) =>
                  setProduct({
                    ...product,
                    availability: e.target.checked
                  })
                }
              />

              Available

            </label>

            <button type="submit">
              Add Product
            </button>

          </form>

        </div>

      )}

      {/* ======================================
          ORDERS
      ====================================== */}

      {page === "orders" && (

        <div className="page">

          <h2>📋 Orders</h2>

          <button
            className="refresh"
            onClick={loadOrders}
          >
            🔄 Refresh Orders
          </button>

          <div className="orders-container">

            {orders.length === 0 ? (

              <p>No orders found.</p>

            ) : (

              <table>

                <thead>

                  <tr>
                    <th>ID</th>
                    <th>Customer</th>
                    <th>Product ID</th>
                    <th>Quantity</th>
                    <th>Total</th>
                    <th>Status</th>
                    <th>Tracking</th>
                  </tr>

                </thead>

                <tbody>

                  {orders.map((item) => (

                    <tr key={item.id}>

                      <td>
                        {item.id}
                      </td>

                      <td>
                        {item.customer_name}
                      </td>

                      <td>
                        {item.product_id}
                      </td>

                      <td>
                        {item.quantity}
                      </td>

                      <td>
                        ₹{item.total_amount}
                      </td>

                      <td>
                        {item.status}
                      </td>

                      <td>
                        {item.tracking_number || "-"}
                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            )}

          </div>

        </div>

      )}

    </div>
  );
}

export default App;