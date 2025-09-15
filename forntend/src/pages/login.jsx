// login.jsx
import Form from "../components/form"

function Login(){
    return <Form route="/api/token/" method="login" showRegisterLink={true} />
}

export default Login
