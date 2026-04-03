import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider }          from './context/AuthContext';
import ProtectedRoute            from './components/ProtectedRoute';
import LoginPage                 from './pages/LoginPage';
import RegisterPage              from './pages/RegisterPage';
import DashboardPage             from './pages/DashboardPage';
import CatalogPage               from './pages/CatalogPage';
import NewProductPage            from './pages/NewProductPage';
import ProductDetailPage         from './pages/ProductDetailPage';
import CartPage                  from './pages/CartPage';
import SellerDashboardPage       from './pages/SellerDashboardPage';
import EditProductPage           from './pages/EditProductPage';
import HomePage                  from './pages/HomePage';
import CheckoutSuccessPage       from './pages/CheckoutSuccessPage';
import CheckoutFailurePage       from './pages/CheckoutFailurePage';
import CheckoutPendingPage       from './pages/CheckoutPendingPage';
import OrdersPage                from './pages/OrdersPage';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login"    element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/" element={<ProtectedRoute />}>
            <Route index element={<HomePage />} />
            <Route path="dashboard"              element={<DashboardPage />} />
            <Route path="catalog"                element={<CatalogPage />} />
            <Route path="products/new"           element={<NewProductPage />} />
            <Route path="products/:id"           element={<ProductDetailPage />} />
            <Route path="products/:id/edit"      element={<EditProductPage />} />
            <Route path="cart"                   element={<CartPage />} />
            <Route path="seller"                 element={<SellerDashboardPage />} />
            <Route path="orders"                 element={<OrdersPage />} />
            <Route path="checkout/success"       element={<CheckoutSuccessPage />} />
            <Route path="checkout/failure"       element={<CheckoutFailurePage />} />
            <Route path="checkout/pending"       element={<CheckoutPendingPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

/*import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider }          from './context/AuthContext';
import ProtectedRoute            from './components/ProtectedRoute';
import LoginPage                 from './pages/LoginPage';
import RegisterPage              from './pages/RegisterPage';
import DashboardPage             from './pages/DashboardPage';
import CatalogPage               from './pages/CatalogPage';
import NewProductPage            from './pages/NewProductPage';
import ProductDetailPage         from './pages/ProductDetailPage';
import CartPage                  from './pages/CartPage';
import SellerDashboardPage       from './pages/SellerDashboardPage';
import EditProductPage           from './pages/EditProductPage';
import HomePage                  from './pages/HomePage';
import CheckoutSuccessPage       from './pages/CheckoutSuccessPage';
import CheckoutFailurePage       from './pages/CheckoutFailurePage';
import CheckoutPendingPage       from './pages/CheckoutPendingPage';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login"    element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/" element={<ProtectedRoute />}>
            <Route index element={<HomePage />} />
            <Route path="dashboard"              element={<DashboardPage />} />
            <Route path="catalog"                element={<CatalogPage />} />
            <Route path="products/new"           element={<NewProductPage />} />
            <Route path="products/:id"           element={<ProductDetailPage />} />
            <Route path="products/:id/edit"      element={<EditProductPage />} />
            <Route path="cart"                   element={<CartPage />} />
            <Route path="seller"                 element={<SellerDashboardPage />} />
            <Route path="checkout/success"       element={<CheckoutSuccessPage />} />
            <Route path="checkout/failure"       element={<CheckoutFailurePage />} />
            <Route path="checkout/pending"       element={<CheckoutPendingPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}*/

/*import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
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
import HomePage               from './pages/HomePage';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login"    element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/" element={<ProtectedRoute />}>
            <Route index element={<HomePage />} />
            <Route path="dashboard"         element={<DashboardPage />} />
            <Route path="catalog"           element={<CatalogPage />} />
            <Route path="products/new"      element={<NewProductPage />} />
            <Route path="products/:id"      element={<ProductDetailPage />} />
            <Route path="products/:id/edit" element={<EditProductPage />} />
            <Route path="cart"              element={<CartPage />} />
            <Route path="seller"            element={<SellerDashboardPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}*/
/*import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
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
}*/
