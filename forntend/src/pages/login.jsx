// login.jsx
import Form from "../components/form"

function Login(){ // Not needed Login component if everything is on Form component
    return <Form route="/api/token/" method="login" showRegisterLink={true} />
}

export default Login
