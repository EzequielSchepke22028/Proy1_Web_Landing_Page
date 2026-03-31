import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import ProductCard from '../components/ProductCard';
import api from '../api/api';

const CATEGORIES = [
  { name: 'Electronics',    icon: 'Ì≤ª', color: 'bg-blue-50 text-blue-600' },
  { name: 'Clothing',       icon: 'Ì±ï', color: 'bg-purple-50 text-purple-600' },
  { name: 'Home & Garden',  icon: 'Ìø°', color: 'bg-green-50 text-green-600' },
  { name: 'Sports',         icon: '‚öΩ', color: 'bg-orange-50 text-orange-600' },
  { name: 'Books',          icon: 'Ì≥ö', color: 'bg-yellow-50 text-yellow-600' },
  { name: 'Toys',           icon: 'Ì∑∏', color: 'bg-pink-50 text-pink-600' },
  { name: 'Vehicles',       icon: 'Ì∫ó', color: 'bg-red-50 text-red-600' },
  { name: 'Other',          icon: 'Ì≥¶', color: 'bg-gray-50 text-gray-600' },
];

export default function HomePage() {
  const navigate = useNavigate();
  const [trending, setTrending]   = useState([]);
  const [recent, setRecent]       = useState([]);
  const [search, setSearch]       = useState('');
  const [loading, setLoading]     = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [trendRes, recentRes] = await Promise.all([
          api.get('/recommendations/trending'),
          api.get('/recommendations/recent'),
        ]);
        setTrending(trendRes.data);
        setRecent(recentRes.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (search.trim()) navigate(`/catalog?search=${encodeURIComponent(search)}`);
    else navigate('/catalog');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      {/* Hero Banner */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white">
        <div className="max-w-7xl mx-auto px-4 py-16 flex flex-col items-center text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Compr√° y vend√© en <span className="text-yellow-300">MarketEze</span>
          </h1>
          <p className="text-blue-100 text-lg mb-8 max-w-xl">
            El marketplace argentino con los mejores productos al mejor precio
          </p>
          <form onSubmit={handleSearch} className="w-full max-w-2xl flex gap-2">
            <input
              type="text"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Buscar productos, marcas y m√°s..."
              className="flex-1 px-5 py-3 rounded-xl text-gray-800 text-lg focus:outline-none focus:ring-4 focus:ring-yellow-300 shadow-lg"
            />
            <button type="submit"
              className="bg-yellow-400 hover:bg-yellow-300 text-gray-900 font-bold px-6 py-3 rounded-xl transition-colors shadow-lg">
              Ì¥ç Buscar
            </button>
          </form>
        </div>
      </div>

      {/* Banners de beneficios */}
      <div className="bg-white border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 py-4 grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { icon: 'Ì∫ö', text: 'Env√≠o gratis', sub: 'En miles de productos' },
            { icon: 'Ì¥í', text: 'Compra segura', sub: 'Pagos protegidos' },
            { icon: '‚Ü©Ô∏è', text: 'Devoluciones', sub: 'Hasta 30 d√≠as' },
            { icon: 'Ì≤≥', text: 'Hasta 18 cuotas', sub: 'Con tarjeta de cr√©dito' },
          ].map((b, i) => (
            <div key={i} className="flex items-center gap-3 p-2">
              <span className="text-2xl">{b.icon}</span>
              <div>
                <p className="font-semibold text-gray-800 text-sm">{b.text}</p>
                <p className="text-gray-400 text-xs">{b.sub}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">

        {/* Categor√≠as */}
        <section className="mb-10">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Explor√° por categor√≠a</h2>
          <div className="grid grid-cols-4 md:grid-cols-8 gap-3">
            {CATEGORIES.map(cat => (
              <Link
                key={cat.name}
                to={`/catalog?category=${encodeURIComponent(cat.name)}`}
                className={`${cat.color} rounded-xl p-3 flex flex-col items-center gap-2 hover:shadow-md transition-shadow`}
              >
                <span className="text-3xl">{cat.icon}</span>
                <span className="text-xs font-medium text-center leading-tight">{cat.name}</span>
              </Link>
            ))}
          </div>
        </section>

        {/* Trending */}
        {!loading && trending.length > 0 && (
          <section className="mb-10">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-800">Ì¥• M√°s vistos hoy</h2>
              <Link to="/catalog" className="text-blue-600 hover:underline text-sm font-medium">
                Ver todos ‚Üí
              </Link>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              {trending.map(p => <ProductCard key={p.id} product={p} />)}
            </div>
          </section>
        )}

        {/* Recientes */}
        {!loading && recent.length > 0 && (
          <section className="mb-10">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-800">Ì∂ï Reci√©n llegados</h2>
              <Link to="/catalog" className="text-blue-600 hover:underline text-sm font-medium">
                Ver todos ‚Üí
              </Link>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              {recent.map(p => <ProductCard key={p.id} product={p} />)}
            </div>
          </section>
        )}

        {loading && (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-10">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="bg-white rounded-xl shadow animate-pulse">
                <div className="aspect-square bg-gray-200 rounded-t-xl" />
                <div className="p-3 space-y-2">
                  <div className="h-3 bg-gray-200 rounded w-full" />
                  <div className="h-4 bg-gray-200 rounded w-1/2" />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* CTA Vendedor */}
        <section className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-2xl p-8 text-white flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <h3 className="text-2xl font-bold mb-2">¬øQuer√©s vender en MarketEze?</h3>
            <p className="text-blue-100">Public√° gratis y lleg√° a miles de compradores en todo el pa√≠s</p>
          </div>
          <Link to="/products/new"
            className="bg-white text-blue-600 font-bold px-8 py-3 rounded-xl hover:bg-blue-50 transition-colors whitespace-nowrap shadow-lg">
            Publicar gratis ‚Üí
          </Link>
        </section>

      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-100 mt-10 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-400 text-sm">
          <p className="font-bold text-gray-600 text-lg mb-2">
            <span className="text-blue-600">Market</span>Eze
          </p>
          <p>¬© 2026 MarketEze ‚Äî Desarrollado por Ezequiel Schepke</p>
          <p className="mt-1">FastAPI + React + TailwindCSS + MercadoPago</p>
        </div>
      </footer>
    </div>
  );
}
