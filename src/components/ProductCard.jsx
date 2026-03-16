import { Link } from 'react-router-dom';

export default function ProductCard({ product }) {
  const { id, title, price, image_url, category, stock, views } = product;

  return (
    <Link to={`/products/${id}`} className="group block">
      <div className="bg-white rounded-xl shadow hover:shadow-md transition-shadow overflow-hidden border border-gray-100">
        <div className="aspect-square bg-gray-100 overflow-hidden">
          {image_url ? (
            <img
              src={image_url}
              alt={title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-300 text-6xl">
              ÌªçÔ∏è
            </div>
          )}
        </div>
        <div className="p-4">
          {category && (
            <span className="text-xs text-blue-600 font-medium uppercase tracking-wide">
              {category}
            </span>
          )}
          <h3 className="text-gray-800 font-semibold mt-1 line-clamp-2 group-hover:text-blue-600 transition-colors">
            {title}
          </h3>
          <p className="text-2xl font-bold text-blue-600 mt-2">
            ${Number(price).toLocaleString('es-AR')}
          </p>
          <div className="flex justify-between items-center mt-3 text-xs text-gray-400">
            <span>{stock > 0 ? `${stock} disponibles` : '‚ö†Ô∏è Sin stock'}</span>
            <span>Ì±Å {views}</span>
          </div>
        </div>
      </div>
    </Link>
  );
}
