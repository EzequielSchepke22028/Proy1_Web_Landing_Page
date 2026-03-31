import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';

export default function CheckoutPendingPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-lg mx-auto px-4 py-20 text-center">
        <div className="bg-white rounded-2xl shadow-lg p-10">
          <div className="text-7xl mb-6">‚è≥</div>
          <h1 className="text-3xl font-bold text-gray-800 mb-3">
            Pago pendiente
          </h1>
          <p className="text-gray-500 mb-6">
            Tu pago est√° siendo procesado. Te notificaremos cuando se confirme.
          </p>
          <div className="bg-yellow-50 border border-yellow-100 rounded-xl p-4 mb-8">
            <p className="text-yellow-700 text-sm font-medium">
              Ìµê Esto puede demorar algunos minutos
            </p>
          </div>
          <div className="flex flex-col gap-3">
            <Link to="/dashboard"
              className="bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700 transition-colors font-semibold">
              Ir al inicio
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
