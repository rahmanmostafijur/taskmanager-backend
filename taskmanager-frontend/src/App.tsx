import './App.css'
import { useState, useEffect } from 'react'

const API = 'https://taskmanager-backend-tclq.onrender.com'

interface Task {
  id: number
  title: string
  description: string | null
  is_done: boolean
}

function App() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [error, setError] = useState("")
  const [tasks, setTasks] = useState<Task[]>([])
  const [newTitle, setNewTitle] = useState("")

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

  async function register() {
    const response = await fetch(API + '/users/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })

    const data = await response.json()

    if (!response.ok) {
      setError(typeof data.detail === 'string' ? data.detail : 'Registration failed')
      return
    }

    setError("")
    login()
  }

  function logout() {
    localStorage.removeItem('token')
    setToken(null)
  }

  async function fetchTasks() {
    const response = await fetch(API + '/tasks/', {
      headers: { 'Authorization': 'Bearer ' + token }
    })
    const data = await response.json()
    setTasks(data)
  }

  async function addTask() {
    await fetch(API + '/tasks/', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ title: newTitle })
    })

    setNewTitle("")
    fetchTasks()
  }

  async function deleteTask(id: number) {
    await fetch(API + '/tasks/' + id, {
      method: 'DELETE',
      headers: { 'Authorization': 'Bearer ' + token }
    })
    fetchTasks()
  }

  async function toggleTask(task: Task) {
    await fetch(API + '/tasks/' + task.id, {
      method: 'PUT',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: task.title,
        is_done: !task.is_done
      })
    })
    fetchTasks()
  }

  useEffect(() => {
    if (token) {
      fetchTasks()
    }
  }, [token])

  return (
    <div className="container">
      <h1>Task Manager</h1>

      {token ? (
        <div>
          <h2>My Tasks</h2>
          <input
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder='New task'
          />
          <button onClick={addTask}>Add</button>
          <ul>
            {tasks.map((task) => (
              <li key={task.id}>
                <input
                  type="checkbox"
                  checked={task.is_done}
                  onChange={() => toggleTask(task)}
                />
                <span
                  className="task-title"
                  style={{ textDecoration: task.is_done ? 'line-through' : 'none' }}
                >
                  {task.title}
                </span>
                <button
                  className="delete-btn"
                  onClick={() => deleteTask(task.id)}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
          <button className="logout-btn" onClick={logout}>Logout</button>
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
          <button onClick={register}>Register</button>
          {error && <p className="error">{error}</p>}
        </div>
      )}
    </div>
  )
}

export default App