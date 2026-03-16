import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';

export default function DashboardPage() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow px-6 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">
          <span className="text-blue-600">Market</span>
          <span className="text-gray-800">Eze</span>
        </h1>
        <div className="flex items-center gap-4">
          <Link to="/catalog" className="text-blue-600 hover:underline font-medium">
            Ver cat√°logo
          </Link>
          <button
            onClick={logout}
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Cerrar sesi√≥n
          </button>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 py-10">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          Hola, {user?.full_name || user?.username} Ì±ã
        </h2>
        <p className="text-gray-500 mb-8">Bienvenido a tu panel de MarketEze</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link to="/catalog" className="bg-white rounded-xl shadow p-6 hover:shadow-md transition-shadow">
            <div className="text-3xl mb-3">ÌªçÔ∏è</div>
            <h3 className="font-semibold text-gray-800">Ver cat√°logo</h3>
            <p className="text-sm text-gray-500 mt-1">Explor√° todos los productos</p>
          </Link>

          <Link to="/products/new" className="bg-white rounded-xl shadow p-6 hover:shadow-md transition-shadow">
            <div className="text-3xl mb-3">‚ûï</div>
            <h3 className="font-semibold text-gray-800">Publicar producto</h3>
            <p className="text-sm text-gray-500 mt-1">Vend√© tus productos</p>
          </Link>

          <div className="bg-white rounded-xl shadow p-6">
            <div className="text-3xl mb-3">Ì±§</div>
            <h3 className="font-semibold text-gray-800">Mi perfil</h3>
            <p className="text-sm text-gray-500 mt-1">@{user?.username}</p>
            <p className="text-sm text-gray-500">{user?.email}</p>
            <span className="inline-block mt-2 text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
              {user?.role}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
