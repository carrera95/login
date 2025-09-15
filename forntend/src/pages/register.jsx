// register.jsx
import Form from "../components/form"

function Register() {
    return <Form route="/api/user/register/" method="register" showLoginLink={true}/>
}

export default Register
