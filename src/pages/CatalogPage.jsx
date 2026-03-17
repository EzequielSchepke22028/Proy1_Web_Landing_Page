import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { getProducts } from '../api/products';
import ProductCard from '../components/ProductCard';
import Navbar from '../components/Navbar';
import api from '../api/api';

const CATEGORIES = [
  'Electronics','Clothing','Home & Garden','Sports',
  'Books','Toys','Vehicles','Services','Other'
];

export default function CatalogPage() {
  const [searchParams] = useSearchParams();
  const [products, setProducts]     = useState([]);
  const [trending, setTrending]     = useState([]);
  const [total, setTotal]           = useState(0);
  const [page, setPage]             = useState(1);
  const [pages, setPages]           = useState(1);
  const [loading, setLoading]       = useState(true);
  const [search, setSearch]         = useState(searchParams.get('search') || '');
  const [category, setCategory]     = useState('');
  const [sortBy, setSortBy]         = useState('created_at');
  const [showTrending, setShowTrending] = useState(true);

  useEffect(() => {
    fetchTrending();
  }, []);

  useEffect(() => {
    fetchProducts();
  }, [page, category, sortBy]);

  const fetchTrending = async () => {
    try {
      const res = await api.get('/recommendations/trending');
      setTrending(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const params = { page, page_size: 12, sort_by: sortBy };
      if (search)   params.search   = search;
      if (category) params.category = category;
      const res = await getProducts(params);
      setProducts(res.data.items);
      setTotal(res.data.total);
      setPages(res.data.pages);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    setShowTrending(false);
    fetchProducts();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 py-8">

        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-800">
            Catálogo <span className="text-blue-600">({total})</span>
          </h1>
          <Link to="/products/new"
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium">
            + Publicar producto
          </Link>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-4 mb-6 flex flex-wrap gap-3">
          <form onSubmit={handleSearch} className="flex gap-2 flex-1 min-w-64">
            <input
              type="text"
              placeholder="Buscar productos..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="border border-gray-200 rounded-lg px-3 py-2 flex-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              Buscar
            </button>
          </form>

          <select
            value={category}
            onChange={e => { setCategory(e.target.value); setPage(1); setShowTrending(false); }}
            className="border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Todas las categorías</option>
            {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>

          <select
            value={sortBy}
            onChange={e => { setSortBy(e.target.value); setPage(1); setShowTrending(false); }}
            className="border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="created_at">Más recientes</option>
            <option value="price">Precio</option>
            <option value="views">Más vistos</option>
          </select>
        </div>

        {showTrending && trending.length > 0 && (
          <div className="mb-10">
            <h2 className="text-xl font-bold text-gray-800 mb-4">🔥 Más vistos</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              {trending.map(p => <ProductCard key={p.id} product={p} />)}
            </div>
            <div className="border-t border-gray-100 mt-8 mb-6" />
          </div>
        )}

        <h2 className="text-xl font-bold text-gray-800 mb-4">Todos los productos</h2>

        {loading ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="bg-white rounded-xl shadow animate-pulse">
                <div className="aspect-square bg-gray-200 rounded-t-xl" />
                <div className="p-4 space-y-2">
                  <div className="h-3 bg-gray-200 rounded w-1/3" />
                  <div className="h-4 bg-gray-200 rounded w-full" />
                  <div className="h-6 bg-gray-200 rounded w-1/2" />
                </div>
              </div>
            ))}
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-20 text-gray-400">
            <p className="text-5xl mb-4">🔍</p>
            <p className="text-lg">No se encontraron productos</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {products.map(p => <ProductCard key={p.id} product={p} />)}
          </div>
        )}

        {pages > 1 && (
          <div className="flex justify-center gap-2 mt-8">
            <button onClick={() => setPage(p => Math.max(1, p-1))} disabled={page===1}
              className="px-4 py-2 rounded-lg border border-gray-200 disabled:opacity-40 hover:bg-gray-50">
              ← Anterior
            </button>
            <span className="px-4 py-2 text-gray-600">{page} / {pages}</span>
            <button onClick={() => setPage(p => Math.min(pages, p+1))} disabled={page===pages}
              className="px-4 py-2 rounded-lg border border-gray-200 disabled:opacity-40 hover:bg-gray-50">
              Siguiente →
            </button>
          </div>
        )}

      </div>
    </div>
  );
}

/*import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { getProducts } from '../api/products';
import ProductCard from '../components/ProductCard';
import Navbar from '../components/Navbar';

const CATEGORIES = [
  'Electronics','Clothing','Home & Garden','Sports',
  'Books','Toys','Vehicles','Services','Other'
];

export default function CatalogPage() {
  const [searchParams] = useSearchParams();
  const [products, setProducts] = useState([]);
  const [total, setTotal]       = useState(0);
  const [page, setPage]         = useState(1);
  const [pages, setPages]       = useState(1);
  const [loading, setLoading]   = useState(true);
  const [search, setSearch]     = useState(searchParams.get('search') || '');
  const [category, setCategory] = useState('');
  const [sortBy, setSortBy]     = useState('created_at');

  useEffect(() => { fetchProducts(); }, [page, category, sortBy]);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const params = { page, page_size: 12, sort_by: sortBy };
      if (search)   params.search   = search;
      if (category) params.category = category;
      const res = await getProducts(params);
      setProducts(res.data.items);
      setTotal(res.data.total);
      setPages(res.data.pages);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchProducts();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 py-8">

        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-800">
            Catálogo <span className="text-blue-600">({total})</span>
          </h1>
          <Link
            to="/products/new"
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            + Publicar producto
          </Link>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-4 mb-6 flex flex-wrap gap-3">
          <form onSubmit={handleSearch} className="flex gap-2 flex-1 min-w-64">
            <input
              type="text"
              placeholder="Buscar productos..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="border border-gray-200 rounded-lg px-3 py-2 flex-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              Buscar
            </button>
          </form>

          <select
            value={category}
            onChange={e => { setCategory(e.target.value); setPage(1); }}
            className="border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Todas las categorías</option>
            {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>

          <select
            value={sortBy}
            onChange={e => { setSortBy(e.target.value); setPage(1); }}
            className="border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="created_at">Más recientes</option>
            <option value="price">Precio</option>
            <option value="views">Más vistos</option>
          </select>
        </div>

        {loading ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="bg-white rounded-xl shadow animate-pulse">
                <div className="aspect-square bg-gray-200 rounded-t-xl" />
                <div className="p-4 space-y-2">
                  <div className="h-3 bg-gray-200 rounded w-1/3" />
                  <div className="h-4 bg-gray-200 rounded w-full" />
                  <div className="h-6 bg-gray-200 rounded w-1/2" />
                </div>
              </div>
            ))}
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-20 text-gray-400">
            <p className="text-5xl mb-4">���</p>
            <p className="text-lg">No se encontraron productos</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {products.map(p => <ProductCard key={p.id} product={p} />)}
          </div>
        )}

        {pages > 1 && (
          <div className="flex justify-center gap-2 mt-8">
            <button onClick={() => setPage(p => Math.max(1, p-1))} disabled={page===1}
              className="px-4 py-2 rounded-lg border border-gray-200 disabled:opacity-40 hover:bg-gray-50">
              ← Anterior
            </button>
            <span className="px-4 py-2 text-gray-600">{page} / {pages}</span>
            <button onClick={() => setPage(p => Math.min(pages, p+1))} disabled={page===pages}
              className="px-4 py-2 rounded-lg border border-gray-200 disabled:opacity-40 hover:bg-gray-50">
              Siguiente →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}*/
