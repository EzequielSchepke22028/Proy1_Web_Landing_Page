import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider }       from './context/AuthContext';
import ProtectedRoute         from './components/ProtectedRoute';
import LoginPage              from './pages/LoginPage';
import RegisterPage           from './pages/RegisterPage';
import DashboardPage          from './pages/DashboardPage';
import CatalogPage            from './pages/CatalogPage';
import NewProductPage         from './pages/NewProductPage';
import ProductDetailPage      from './pages/ProductDetailPage';
import CartPage               from './pages/CartPage';
import SellerDashboardPage    from './pages/SellerDashboardPage';
import EditProductPage        from './pages/EditProductPage';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login"    element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/" element={<ProtectedRoute />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard"        element={<DashboardPage />} />
            <Route path="catalog"          element={<CatalogPage />} />
            <Route path="products/new"     element={<NewProductPage />} />
            <Route path="products/:id"     element={<ProductDetailPage />} />
            <Route path="products/:id/edit" element={<EditProductPage />} />
            <Route path="cart"             element={<CartPage />} />
            <Route path="seller"           element={<SellerDashboardPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
