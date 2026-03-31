import { useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import useCartStore from '../store/cartStore';
import Navbar from '../components/Navbar';

export default function CheckoutSuccessPage() {
  const [searchParams] = useSearchParams();
  const clearCart = useCartStore(s => s.clearCart);
  const paymentId = searchParams.get('payment_id');

  useEffect(() => {
    clearCart();
  }, [clearCart]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-lg mx-auto px-4 py-20 text-center">
        <div className="bg-white rounded-2xl shadow-lg p-10">
          <div className="text-7xl mb-6 animate-bounce">🎉</div>
          <h1 className="text-3xl font-bold text-gray-800 mb-3">
            ¡Pago exitoso!
          </h1>
          <p className="text-gray-500 mb-2">
            Tu compra fue procesada correctamente.
          </p>
          {paymentId && (
            <p className="text-xs text-gray-400 mb-6">
              ID de pago: <span className="font-mono">{paymentId}</span>
            </p>
          )}
          <div className="bg-green-50 border border-green-100 rounded-xl p-4 mb-8">
            <p className="text-green-700 text-sm font-medium">
              ✅ Recibirás un email con los detalles de tu compra
            </p>
          </div>
          <div className="flex flex-col gap-3">
            <Link to="/catalog"
              className="bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700 transition-colors font-semibold">
              Seguir comprando
            </Link>
            <Link to="/"
              className="border border-gray-200 text-gray-600 py-3 rounded-xl hover:bg-gray-50 transition-colors">
              Ir al inicio
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}