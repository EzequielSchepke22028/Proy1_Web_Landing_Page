import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import api from '../api/api';
import { useAuth } from '../context/AuthContext';

export default function SellerDashboardPage() {
  const { user } = useAuth();
  const [products, setProducts] = useState([]);
  const [loading, setLoading]   = useState(true);
  const [stats, setStats]       = useState({ total: 0, active: 0, views: 0 });

  useEffect(() => { fetchMyProducts(); }, []);

  const fetchMyProducts = async () => {
    setLoading(true);
    try {
      const res = await api.get('/products/mine');
      setProducts(res.data);
      setStats({
        total:  res.data.length,
        active: res.data.filter(p => p.is_active).length,
        views:  res.data.reduce((sum, p) => sum + p.views, 0),
      });
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const toggleProduct = async (id, isActive) => {
    try {
      await api.patch(`/products/${id}`, { is_active: !isActive });
      fetchMyProducts();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 py-8">

        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Panel del vendedor</h1>
            <p className="text-gray-500 text-sm mt-1">Hola {user?.full_name}</p>
          </div>
          <Link
            to="/products/new"
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            + Publicar producto
          </Link>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-white rounded-xl shadow p-5 text-center">
            <p className="text-3xl font-bold text-blue-600">{stats.total}</p>
            <p className="text-gray-500 text-sm mt-1">Productos totales</p>
          </div>
          <div className="bg-white rounded-xl shadow p-5 text-center">
            <p className="text-3xl font-bold text-green-600">{stats.active}</p>
            <p className="text-gray-500 text-sm mt-1">Activos</p>
          </div>
          <div className="bg-white rounded-xl shadow p-5 text-center">
            <p className="text-3xl font-bold text-purple-600">{stats.views}</p>
            <p className="text-gray-500 text-sm mt-1">Vistas totales</p>
          </div>
        </div>

        {loading ? (
          <div className="space-y-3">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="bg-white rounded-xl shadow p-4 animate-pulse h-20" />
            ))}
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-20 text-gray-400">
            <p className="text-5xl mb-4">📦</p>
            <p className="text-lg">No publicaste ningun producto todavia</p>
            <Link to="/products/new" className="text-blue-600 hover:underline mt-2 block">
              Publicar mi primer producto
            </Link>
          </div>
        ) : (
          <div className="bg-white rounded-xl shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-100">
                <tr>
                  <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Producto</th>
                  <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Precio</th>
                  <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Stock</th>
                  <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Vistas</th>
                  <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Estado</th>
                  <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Acciones</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {products.map(p => (
                  <tr key={p.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
                          {p.image_url
                            ? <img src={p.image_url} alt={p.title} className="w-full h-full object-contain" />
                            : <div className="w-full h-full flex items-center justify-center text-lg">🛍️</div>
                          }
                        </div>
                        <div>
                          <p className="font-medium text-gray-800 line-clamp-1">{p.title}</p>
                          <p className="text-xs text-gray-400">{p.category}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-blue-600 font-semibold">
                      ${Number(p.price).toLocaleString('es-AR')}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`text-sm font-medium ${p.stock > 0 ? 'text-green-600' : 'text-red-500'}`}>
                        {p.stock}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-gray-500 text-sm">{p.views}</td>
                    <td className="px-6 py-4">
                      <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                        p.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'
                      }`}>
                        {p.is_active ? 'Activo' : 'Inactivo'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex gap-3">
                        <Link to={`/products/${p.id}`}
                          className="text-xs text-blue-600 hover:underline">Ver</Link>
                        <Link to={`/products/${p.id}/edit`}
                          className="text-xs text-green-600 hover:underline">Editar</Link>
                        <button
                          onClick={() => toggleProduct(p.id, p.is_active)}
                          className="text-xs text-gray-500 hover:text-red-500">
                          {p.is_active ? 'Desactivar' : 'Activar'}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}