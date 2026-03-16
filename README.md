# MarketEze - Marketplace Full Stack

Desarrollado por Ezequiel Schepke - Analista de Sistemas | Fullstack | Data Science

## Como levantar el proyecto

Terminal 1 - Docker:
  docker-compose -f /c/Dev/claude/Proy1_Web_Moderna_Completa/docker-compose.yml up -d

Terminal 2 - Backend:
  source /c/Dev/claude/Proy1_Web_Moderna_Completa/.venv/Scripts/activate
  cd /c/Dev/claude/Proy1_Web_Moderna_Completa/backend
  uvicorn main:app --reload --port 8080

Terminal 3 - Frontend:
  cd /c/Dev/claude/Proy1_Web_Moderna_Completa/frontend
  npm start

URLs: http://localhost:3000 | http://127.0.0.1:8080/docs

## Stack
- Frontend: React 18 + Tailwind CSS + Zustand
- Backend: Python + FastAPI + SQLAlchemy
- DB: PostgreSQL 15 (Docker)
- Auth: JWT + Bcrypt
- Pagos: MercadoPago Checkout Pro

## Semanas completadas
- Semana 1-2: Auth JWT + Catalogo + CRUD productos
- Semana 3: Navbar + Detalle producto + Carrito Zustand
- Semana 4: MercadoPago Checkout Pro

## Proximas semanas
- Semana 5: Panel vendedor + ordenes
- Semana 6: Data Science + recomendaciones
- Semana 7: Automatizaciones n8n
- Semana 8: Deploy VPS + dominio
