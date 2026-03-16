import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getProduct } from '../api/products';

export default function ProductDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState('');

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await getProduct(id);
        setProduct(res.data);
      } catch (e) {
        setError('Producto no encontrado');
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, [id]);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600" />
    </div>
  );

  if (error) return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4">
      <p className="text-gray-500 text-lg">{error}</p>
      <Link to="/catalog" className="text-blue-600 hover:underline">Volver al cat√°logo</Link>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow px-6 py-4 flex items-center gap-4">
        <button onClick={() => navigate(-1)} className="text-gray-500 hover:text-gray-800">
          ‚Üê Volver
        </button>
        <Link to="/catalog" className="text-blue-600 hover:underline text-sm">Cat√°logo</Link>
      </nav>

      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="bg-white rounded-2xl shadow overflow-hidden">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-0">

            <div className="bg-gray-100 flex items-center justify-center p-8 min-h-80">
              {product.image_url ? (
                <img
                  src={product.image_url}
                  alt={product.title}
                  className="max-h-80 object-contain"
                />
              ) : (
                <div className="text-gray-300 text-8xl">ÌªçÔ∏è</div>
              )}
            </div>

            <div className="p-8 flex flex-col justify-between">
              <div>
                {product.category && (
                  <span className="text-xs text-blue-600 font-semibold uppercase tracking-wide">
                    {product.category}
                  </span>
                )}
                <h1 className="text-2xl font-bold text-gray-800 mt-2 mb-4">
                  {product.title}
                </h1>
                {product.description && (
                  <p className="text-gray-600 mb-6">{product.description}</p>
                )}
                <div className="flex items-center gap-4 text-sm text-gray-400 mb-6">
                  <span>Ì±Å {product.views} vistas</span>
                  <span>Ì≥¶ {product.sold_count} vendidos</span>
                </div>
              </div>

              <div>
                <p className="text-4xl font-bold text-blue-600 mb-2">
                  ${Number(product.price).toLocaleString('es-AR')}
                </p>
                <p className={`text-sm mb-6 ${product.stock > 0 ? 'text-green-600' : 'text-red-500'}`}>
                  {product.stock > 0 ? `‚úì ${product.stock} disponibles` : '‚úó Sin stock'}
                </p>

                <button
                  disabled={product.stock === 0}
                  className="w-full bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-50 font-semibold text-lg"
                >
                  Agregar al carrito
                </button>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}
