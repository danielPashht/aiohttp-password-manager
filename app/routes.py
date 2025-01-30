from .handlers import (
    register, login,
    generate_password,
    get_passwords,
    delete_password
)


def setup_routes(app):
    app.router.add_post("/register", register)
    app.router.add_post("/login", login)
    app.router.add_post("/password/generate", generate_password)
    app.router.add_get("/passwords", get_passwords)
    app.router.add_delete("/password/{password_id:\\d+}", delete_password)
