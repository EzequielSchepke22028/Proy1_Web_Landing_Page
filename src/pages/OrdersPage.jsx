import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import api from '../api/api';

const STATUS_LABELS = {
  pending:   { label: 'Pendiente',   color: 'bg-yellow-100 text-yellow-700' },
  paid:      { label: 'Pagado',      color: 'bg-green-100 text-green-700' },
  shipped:   { label: 'Enviado',     color: 'bg-blue-100 text-blue-700' },
  delivered: { label: 'Entregado',   color: 'bg-purple-100 text-purple-700' },
  cancelled: { label: 'Cancelado',   color: 'bg-red-100 text-red-700' },
};

export default function OrdersPage() {
  const [orders, setOrders]   = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const res = await api.get('/orders/mine');
        setOrders(res.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Mis compras</h1>

        {loading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="bg-white rounded-xl shadow p-6 animate-pulse h-32" />
            ))}
          </div>
        ) : orders.length === 0 ? (
          <div className="text-center py-20 text-gray-400">
            <p className="text-5xl mb-4">Ì≥¶</p>
            <p className="text-lg mb-2">Todav√≠a no hiciste ninguna compra</p>
            <Link to="/catalog" className="text-blue-600 hover:underline">
              Ver cat√°logo
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {orders.map(order => {
              const status = STATUS_LABELS[order.status] || STATUS_LABELS.pending;
              return (
                <div key={order.id} className="bg-white rounded-xl shadow overflow-hidden">
                  <div className="flex justify-between items-center px-6 py-4 border-b border-gray-50">
                    <div>
                      <p className="text-sm text-gray-400">
                        Orden #{order.id} ¬∑ {new Date(order.created_at).toLocaleDateString('es-AR', {
                          day: '2-digit', month: 'long', year: 'numeric'
                        })}
                      </p>
                      {order.mp_payment_id && (
                        <p className="text-xs text-gray-300 font-mono">
                          Pago: {order.mp_payment_id}
                        </p>
                      )}
                    </div>
                    <div className="flex items-center gap-4">
                      <span className={`text-xs px-3 py-1 rounded-full font-medium ${status.color}`}>
                        {status.label}
                      </span>
                      <span className="font-bold text-blue-600 text-lg">
                        ${Number(order.total_amount).toLocaleString('es-AR')}
                      </span>
                    </div>
                  </div>
                  <div className="px-6 py-4 space-y-3">
                    {order.items.map(item => (
                      <div key={item.id} className="flex items-center gap-4">
                        <div className="w-12 h-12 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
                          {item.product_image
                            ? <img src={item.product_image} alt={item.product_title}
                                className="w-full h-full object-contain" />
                            : <div className="w-full h-full flex items-center justify-center text-xl">ÌªçÔ∏è</div>
                          }
                        </div>
                        <div className="flex-1">
                          <p className="font-medium text-gray-800 line-clamp-1">
                            {item.product_title}
                          </p>
                          <p className="text-sm text-gray-400">
                            {item.quantity} x ${Number(item.unit_price).toLocaleString('es-AR')}
                          </p>
                        </div>
                        <Link to={`/products/${item.product_id}`}
                          className="text-xs text-blue-600 hover:underline">
                          Ver producto
                        </Link>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
