import './App.css'
import { useState } from 'react'

const API = 'https://taskmanager-backend-tclq.onrender.com'

function App() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [error, setError] = useState("")

  async function login() {
    const response = await fetch(API + '/users/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username, password })
    })

    const data = await response.json()

    if (!response.ok) {
      setError(data.detail)
      return
    }

    setError("")
    localStorage.setItem('token', data.access_token)
    setToken(data.access_token)
  }

  function logout() {
    localStorage.removeItem('token')
    setToken(null)
  }

  return (
    <div>
      <h1>Task Manager</h1>

      {token ? (
        <div>
          <h2>My Tasks</h2>
          <button onClick={logout}>Logout</button>
        </div>
      ) : (
        <div>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder='Username'
          />
          <input
            type='password'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder='Password'
          />
          <button onClick={login}>Login</button>
          {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
      )}
    </div>
  )
}

export default App