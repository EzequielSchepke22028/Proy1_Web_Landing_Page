import { Link, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import useCartStore from '../store/cartStore';

export default function CartPage() {
  const { items, removeItem, updateQuantity, clearCart, getTotalPrice } = useCartStore();
  const navigate = useNavigate();

  if (items.length === 0) return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-3xl mx-auto px-4 py-20 text-center">
        <p className="text-6xl mb-4">Ìªí</p>
        <h2 className="text-xl font-semibold text-gray-700 mb-2">Tu carrito est√° vac√≠o</h2>
        <p className="text-gray-400 mb-6">Agreg√° productos desde el cat√°logo</p>
        <Link to="/catalog" className="bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 transition-colors font-medium">
          Ver cat√°logo
        </Link>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-800">Ìªí Mi carrito</h1>
          <button onClick={clearCart} className="text-sm text-red-500 hover:underline">
            Vaciar carrito
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2 space-y-4">
            {items.map(item => (
              <div key={item.id} className="bg-white rounded-xl shadow p-4 flex gap-4 items-center">
                <div className="w-20 h-20 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
                  {item.image_url ? (
                    <img src={item.image_url} alt={item.title} className="w-full h-full object-contain" />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-2xl">ÌªçÔ∏è</div>
                  )}
                </div>
                <div className="flex-1">
                  <h3 className="font-medium text-gray-800 line-clamp-1">{item.title}</h3>
                  <p className="text-blue-600 font-bold">${Number(item.price).toLocaleString('es-AR')}</p>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => updateQuantity(item.id, item.quantity - 1)}
                    className="w-8 h-8 rounded-full border border-gray-200 hover:bg-gray-100 font-bold"
                  >
                    -
                  </button>
                  <span className="w-8 text-center font-medium">{item.quantity}</span>
                  <button
                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    className="w-8 h-8 rounded-full border border-gray-200 hover:bg-gray-100 font-bold"
                  >
                    +
                  </button>
                </div>
                <button onClick={() => removeItem(item.id)} className="text-red-400 hover:text-red-600 ml-2">
                  ‚úï
                </button>
              </div>
            ))}
          </div>

          <div className="bg-white rounded-xl shadow p-6 h-fit">
            <h2 className="font-bold text-gray-800 text-lg mb-4">Resumen</h2>
            <div className="space-y-2 mb-4">
              {items.map(item => (
                <div key={item.id} className="flex justify-between text-sm text-gray-600">
                  <span className="line-clamp-1 flex-1">{item.title} x{item.quantity}</span>
                  <span className="ml-2">${(Number(item.price) * item.quantity).toLocaleString('es-AR')}</span>
                </div>
              ))}
            </div>
            <div className="border-t pt-4">
              <div className="flex justify-between font-bold text-lg">
                <span>Total</span>
                <span className="text-blue-600">${getTotalPrice().toLocaleString('es-AR')}</span>
              </div>
            </div>
            <button className="w-full bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700 transition-colors font-semibold mt-4">
              Iniciar compra
            </button>
            <Link to="/catalog" className="block text-center text-sm text-gray-400 hover:text-gray-600 mt-3">
              Seguir comprando
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
