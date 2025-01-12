from app import create_app, db
from app.models import User  # Asegúrate de importar el modelo
from werkzeug.security import generate_password_hash  # Importa esto

app = create_app()

# Inicializar la base de datos y agregar datos de prueba
with app.app_context():
    db.create_all()  # Esto crea las tablas en la base de datos
    print("Base de datos inicializada")
    
    # Insertar un usuario de prueba
    if not User.query.filter_by(username="testuser").first():
        new_user = User(
            username="testuser",
            email="test@example.com",
            password_hash=generate_password_hash("password123")  # Genera un hash de la contraseña
        )
        db.session.add(new_user)
        db.session.commit()
        print("Usuario de prueba agregado")

if __name__ == "__main__":
    app.run(debug=True)
