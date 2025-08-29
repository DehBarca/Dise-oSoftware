from tarea4pilares import (
    Usuario, Ubicacion, SensorTemperatura, SensorVibracion, SensorHumedad,
    NotificadorEmail, NotificadorWebhook, NotificadorSMS, GestorAlertas
)

def main():
    # Crear usuarios y ubicaciones
    usuario1 = Usuario(nombre="Ana", email="ana@email.com")
    ubicacion1 = Ubicacion(latitud=19.4326, longitud=-99.1332)

    # Crear sensores
    temp = SensorTemperatura(id="T1", propietario=usuario1, ubicacion=ubicacion1)
    vib = SensorVibracion(id="V1", propietario=usuario1, ubicacion=ubicacion1)
    hum = SensorHumedad(id="H1", propietario=usuario1, ubicacion=ubicacion1)

    # Simular lecturas
    for v in [70, 75, 85, 90, 95]:
        temp.leer(v)
    for v in [1.0, 2.0, 2.6, 3.0]:
        vib.leer(v)
    for v in [50, 55, 65, 70]:
        hum.leer(v)

    # Crear notificadores
    email = NotificadorEmail(destinatario="alertas@email.com")
    webhook = NotificadorWebhook(url="https://webhook.site/xyz")
    sms = NotificadorSMS(numero="5551234567")

    # Crear gestor de alertas
    gestor = GestorAlertas(
        sensores=[temp, vib, hum],
        notificadores=[email, webhook, sms]
    )

    # Evaluar y notificar
    gestor.evaluar_y_notificar()

if __name__ == "__main__":
    main()
