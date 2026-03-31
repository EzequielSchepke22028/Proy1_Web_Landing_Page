import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';

export default function CheckoutFailurePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-lg mx-auto px-4 py-20 text-center">
        <div className="bg-white rounded-2xl shadow-lg p-10">
          <div className="text-7xl mb-6">���</div>
          <h1 className="text-3xl font-bold text-gray-800 mb-3">
            El pago no se procesó
          </h1>
          <p className="text-gray-500 mb-6">
            Hubo un problema con tu pago. No se realizó ningún cargo.
          </p>
          <div className="bg-red-50 border border-red-100 rounded-xl p-4 mb-8">
            <p className="text-red-700 text-sm font-medium">
              ❌ Podés intentarlo de nuevo o usar otro método de pago
            </p>
          </div>
          <div className="flex flex-col gap-3">
            <Link to="/cart"
              className="bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700 transition-colors font-semibold">
              Volver al carrito
            </Link>
            <Link to="/catalog"
              className="border border-gray-200 text-gray-600 py-3 rounded-xl hover:bg-gray-50 transition-colors">
              Seguir comprando
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
