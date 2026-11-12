from app import crear_app

app = crear_app()

# Flask busca la variable "app" cuando arranca desde consola.
# Para correr en local: python run.py
if __name__ == "__main__":
    app.run(debug=True)
