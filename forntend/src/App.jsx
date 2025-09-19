import react from 'react'
import { BrowserRouter, Routes, Route, Navigate} from 'react-router-dom'

import Home from './pages/home'
import Login from './pages/login'
import Register from './pages/register'
import NotFound from './pages/notFound'
import ProtectedRoute from './components/protectedRoute'

function LogOut() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogOut() { // Do it in Logout component (create one)
  localStorage.clear()
  return <Register />
}

function App() {
  return (
      <BrowserRouter> 
        <Routes>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />

          <Route 
            path='/login' 
            element={<Login />}>
          </Route>

          <Route 
            path='/logout' 
            element={<LogOut />}>
          </Route>


          <Route 
            path='/register' 
            element={<RegisterAndLogOut />}>
          </Route>

          <Route 
            path="*" 
            element={<NotFound />}>
          </Route>

        </Routes> 
      </BrowserRouter>
  )
}

export default App
