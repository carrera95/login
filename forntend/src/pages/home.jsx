import { useState, useEffect } from "react"
import api from "../api"
import Note from "../components/Note"

import "../styles/Home.css"
 
function Home(){
    const [notes, setNotes] = useState([])
    const [content, setContent] = useState("")
    const [title, setTitle] = useState("")
    const [currentUser, setCurrentUser] = useState(null)
    const [isAdmin, setIsAdmin] = useState(false)

    useEffect(() =>{
        getNotes()
        getCurrentUser()
    }, [])

    const getCurrentUser = () => {
        api
            .get("/api/user/me/")
            .then((res) => {
                setCurrentUser(res.data)
                setIsAdmin(res.data.is_admin)
                console.log("Current user:", res.data) // Just for delepment, never production
            })
            .catch((err) => console.log("Error fetching user:", err))
    }

    const getNotes = () => {
        api
            .get("/api/notes/")
            .then((res) => res.data)
            .then((data) => {setNotes(data); console.log(data)})
            .catch((err) => alert(err)) 
    }

    const deleteNode = (id) => {
        if (!isAdmin) {
            alert("Only administrators can delete notes") 
            return
        }
        
        if (window.confirm("¿Seguro que quieres eliminar esta nota?")) {
            api.delete(`/api/notes/delete/${id}/`)
                .then((res) => {
                    if (res.status === 204) {
                        alert("Nota eliminada")
                        getNotes() 
                    } else {
                        alert("Error al eliminar la nota") 
                    }
                })
                .catch((error) => {
                    console.error("Delete error:", error)
                    if (error.response?.status === 403) {
                        alert("You don't have permission to delete this note")
                    } else {
                        alert("Error deleting note")
                    }
                })
        }
    }   

    const createNote = (e) => {
        e.preventDefault()
        api
            .post("/api/notes/", {content, title})
            .then((res) => {
                if(res.status === 201) {
                    alert("Nota creada")
                    setTitle("") 
                    setContent("")
                    getNotes() 
                } else {
                    alert("Error al crear nota")
                }
            })
            .catch((err) => {
                console.error("Create note error:", err)
                alert("Error creating note")
            })
    }

    return (
        <div>
            <p><a href="../logout" class="top-left-link">LogOut</a></p>
            <div className="user-info">
                <h1>¡Bienvenid@, {currentUser?.username}!</h1>
                {isAdmin && <p className="admin-badge">Administrador</p>}
            </div>
            
            <div> // Apply some style
                <h2>Notas</h2>
                <p>Mostrando {notes.length} nota(s)</p>
                {notes.map((note) => (
                    <Note 
                        note={note} 
                        onDelete={deleteNode} 
                        key={note.id}
                        showDeleteButton={isAdmin}
                        currentUserId={currentUser?.id}
                    />
                ))}
            </div>

            <h2>Crear una nueva nota</h2>
            <form onSubmit={createNote}>
                <label htmlFor="title">Encabezado</label>
                <br />
                <input 
                    type="text" 
                    id="title" 
                    name="title" 
                    required 
                    onChange={(e) => setTitle(e.target.value)}
                    value={title}
                />
                <label htmlFor="content">Contenido</label>
                <br />
                <textarea 
                    id="content" 
                    name="content" 
                    required 
                    value={content} 
                    onChange={(e) => setContent(e.target.value)}>        
                </textarea>
                <br />
                <input type="submit" value="Create Note"></input>
            </form>
        </div>
    )
}

export default Home