import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import useCartStore from '../store/cartStore';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const totalItems = useCartStore(s => s.getTotalItems());

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) =>
    location.pathname === path
      ? 'text-blue-600 font-semibold'
      : 'text-gray-600 hover:text-blue-600 transition-colors';

  return (
    <nav className="bg-white shadow-sm border-b border-gray-100 px-6 py-3 flex items-center justify-between sticky top-0 z-50">
      <Link to="/dashboard" className="text-2xl font-bold">
        <span className="text-blue-600">Market</span>
        <span className="text-gray-800">Eze</span>
      </Link>
      <div className="flex-1 max-w-md mx-6">
        <input
          type="text"
          placeholder="Buscar productos..."
          onKeyDown={e => { if (e.key === 'Enter') navigate('/catalog?search=' + e.target.value); }}
          className="w-full border border-gray-200 rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div className="flex items-center gap-6">
        <Link to="/catalog" className={'text-sm ' + isActive('/catalog')}>Catalogo</Link>
        <Link to="/orders" className="text-gray-600 hover:text-blue-600 transition-colors">Mis compras</Link>
        <Link to="/products/new" className={'text-sm ' + isActive('/products/new')}>Publicar</Link>
        <Link to="/cart" className="relative text-gray-600 hover:text-blue-600">
          <span>Carrito</span>
          {totalItems > 0 && (
            <span className="absolute -top-2 -right-2 bg-blue-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold">
              {totalItems}
            </span>
          )}
        </Link>
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-semibold text-sm">
            {user?.username?.[0]?.toUpperCase()}
          </div>
          <span className="text-sm text-gray-700 hidden md:block">{user?.username}</span>
        </div>
        <button onClick={handleLogout} className="text-sm text-gray-500 hover:text-red-500">Salir</button>
      </div>
    </nav>
  );
}