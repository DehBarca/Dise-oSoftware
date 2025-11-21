import json
from datetime import datetime
from abc import ABC, abstractmethod

# ========== INTERFACES ==========
class INotifier(ABC):
    @abstractmethod
    def send(self, customer: dict, order_id: str, total: float) -> dict:
        pass
    
    @abstractmethod
    def get_notification_type(self) -> str:
        pass

# ========== NOTIFICADORES (SOLID: S, O, D) ==========
class EmailNotifier(INotifier):
    def send(self, customer: dict, order_id: str, total: float) -> dict:
        message = f"Estimado {customer['name']}, su pedido #{order_id} por ${total} ha sido confirmado."
        print(f"📧 EMAIL enviado a {customer['email']}: {message}\n")
        
        return {
            'type': 'email',
            'to': customer['email'],
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_notification_type(self) -> str:
        return 'email'

class SMSNotifier(INotifier):
    def send(self, customer: dict, order_id: str, total: float) -> dict:
        message = f"Pedido #{order_id} confirmado. Total: ${total}. Gracias!"
        print(f"📱 SMS enviado a {customer['phone']}: {message}\n")
        
        return {
            'type': 'sms',
            'to': customer['phone'],
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_notification_type(self) -> str:
        return 'sms'

class PushNotifier(INotifier):
    def send(self, customer: dict, order_id: str, total: float) -> dict:
        message = f"¡Pedido confirmado! #{order_id} - ${total}"
        print(f"🔔 PUSH enviada a {customer['device_id']}: {message}\n")
        
        return {
            'type': 'push',
            'to': customer['device_id'],
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_notification_type(self) -> str:
        return 'push'

# ========== PATRÓN FACTORY (Creacional) ==========
class NotificationFactory:
    def __init__(self):
        self._notifiers = {
            'email': EmailNotifier(),
            'sms': SMSNotifier(),
            'push': PushNotifier()
        }
    
    def get_notifier(self, notification_type: str) -> INotifier:
        notifier = self._notifiers.get(notification_type)
        if not notifier:
            raise ValueError(f"Tipo no soportado: {notification_type}")
        return notifier
    
    def register_notifier(self, notification_type: str, notifier: INotifier):
        self._notifiers[notification_type] = notifier

class NotificationLogger:
    def __init__(self):
        self.notifications_sent = []
    
    def log(self, notification_data: dict):
        self.notifications_sent.append(notification_data)
    
    def get_history(self) -> list:
        return self.notifications_sent

# ========== PATRÓN SINGLETON (Creacional) ==========
class NotificationConfig:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not NotificationConfig._initialized:
            self.max_retries = 3
            self.timeout = 30
            self.enable_logging = True
            self.batch_size = 10
            NotificationConfig._initialized = True
    
    def get_config(self):
        return {
            'max_retries': self.max_retries,
            'timeout': self.timeout,
            'enable_logging': self.enable_logging,
            'batch_size': self.batch_size
        }

# ========== PATRÓN BUILDER (Creacional) ==========
class OrderBuilder:
    def __init__(self):
        self._order_id = None
        self._customer_name = None
        self._customer_email = None
        self._customer_phone = None
        self._customer_device_id = None
        self._total = 0.0
        self._items = []
    
    def with_order_id(self, order_id: str):
        self._order_id = order_id
        return self
    
    def with_customer(self, name: str, email: str, phone: str = None, device_id: str = None):
        self._customer_name = name
        self._customer_email = email
        self._customer_phone = phone
        self._customer_device_id = device_id
        return self
    
    def with_total(self, total: float):
        self._total = total
        return self
    
    def add_item(self, item_name: str, price: float, quantity: int):
        self._items.append({
            'name': item_name,
            'price': price,
            'quantity': quantity
        })
        return self
    
    def build(self) -> dict:
        if not self._order_id or not self._customer_name:
            raise ValueError("Order ID y Customer Name requeridos")
        
        return {
            'order_id': self._order_id,
            'customer': {
                'name': self._customer_name,
                'email': self._customer_email,
                'phone': self._customer_phone,
                'device_id': self._customer_device_id
            },
            'total': self._total,
            'items': self._items
        }

# ========== PATRÓN DECORATOR (Estructural) ==========
class NotifierDecorator(INotifier):
    def __init__(self, notifier: INotifier):
        self._notifier = notifier
    
    def send(self, customer: dict, order_id: str, total: float) -> dict:
        return self._notifier.send(customer, order_id, total)
    
    def get_notification_type(self) -> str:
        return self._notifier.get_notification_type()


class RetryDecorator(NotifierDecorator):
    def __init__(self, notifier: INotifier, max_retries: int = 3):
        super().__init__(notifier)
        self.max_retries = max_retries
    
    def send(self, customer: dict, order_id: str, total: float) -> dict:
        for attempt in range(self.max_retries):
            try:
                print(f"   🔄 Intento {attempt + 1}/{self.max_retries}")
                return self._notifier.send(customer, order_id, total)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                print(f"   ⚠️ Error intento {attempt + 1}: {e}")
        return {}


class LoggingDecorator(NotifierDecorator):
    def send(self, customer: dict, order_id: str, total: float) -> dict:
        print(f"   📝 [LOG] Iniciando {self.get_notification_type()}")
        result = self._notifier.send(customer, order_id, total)
        print(f"   📝 [LOG] Completado")
        return result

# ========== PATRÓN COMPOSITE (Estructural) ==========
class CompositeNotifier(INotifier):
    def __init__(self, name: str):
        self._name = name
        self._notifiers = []
    
    def add(self, notifier: INotifier):
        self._notifiers.append(notifier)
    
    def remove(self, notifier: INotifier):
        self._notifiers.remove(notifier)
    
    def send(self, customer: dict, order_id: str, total: float) -> dict:
        results = []
        print(f"📦 Grupo '{self._name}':")
        
        for notifier in self._notifiers:
            results.append(notifier.send(customer, order_id, total))
        
        return {
            'type': 'composite',
            'group': self._name,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_notification_type(self) -> str:
        return f"composite_{self._name}"

# ========== PATRÓN OBSERVER (Comportamiento) ==========
class INotificationObserver(ABC):
    @abstractmethod
    def update(self, notification_data: dict):
        pass


class AnalyticsObserver(INotificationObserver):
    def __init__(self):
        self.notification_count = {}
    
    def update(self, notification_data: dict):
        notif_type = notification_data.get('type', 'unknown')
        self.notification_count[notif_type] = self.notification_count.get(notif_type, 0) + 1
        print(f"   📊 [Analytics] {notif_type} registrado. Total: {self.notification_count[notif_type]}")
    
    def get_stats(self):
        return self.notification_count


class AuditObserver(INotificationObserver):
    def __init__(self):
        self.audit_log = []
    
    def update(self, notification_data: dict):
        self.audit_log.append({
            'timestamp': datetime.now().isoformat(),
            'notification_type': notification_data.get('type'),
            'recipient': notification_data.get('to'),
            'status': 'sent'
        })
        print(f"   🔍 [Audit] {notification_data.get('type')} → {notification_data.get('to')}")

# ========== PATRÓN CHAIN OF RESPONSIBILITY (Comportamiento) ==========
class IValidator(ABC):
    def __init__(self):
        self._next_validator = None
    
    def set_next(self, validator: 'IValidator'):
        self._next_validator = validator
        return validator
    
    @abstractmethod
    def validate(self, order_data: dict) -> bool:
        pass
    
    def _call_next(self, order_data: dict) -> bool:
        if self._next_validator:
            return self._next_validator.validate(order_data)
        return True


class OrderIdValidator(IValidator):
    def validate(self, order_data: dict) -> bool:
        if not order_data.get('order_id'):
            print("   ❌ Order ID faltante")
            return False
        print("   ✅ Order ID válido")
        return self._call_next(order_data)


class CustomerValidator(IValidator):
    def validate(self, order_data: dict) -> bool:
        customer = order_data.get('customer', {})
        if not customer.get('name') or not customer.get('email'):
            print("   ❌ Cliente incompleto")
            return False
        print("   ✅ Cliente válido")
        return self._call_next(order_data)


class TotalValidator(IValidator):
    def validate(self, order_data: dict) -> bool:
        if order_data.get('total', 0) <= 0:
            print("   ❌ Total inválido")
            return False
        print("   ✅ Total válido")
        return self._call_next(order_data)

# ========== SISTEMA PRINCIPAL ==========
class OrderNotificationSystem:
    def __init__(self, factory: NotificationFactory = None, logger: NotificationLogger = None):
        self.factory = factory or NotificationFactory()
        self.logger = logger or NotificationLogger()
        self._observers = []
        self._validator_chain = self._build_validator_chain()
    
    def _build_validator_chain(self):
        order_id = OrderIdValidator()
        customer = CustomerValidator()
        total = TotalValidator()
        
        order_id.set_next(customer).set_next(total)
        return order_id
    
    def attach_observer(self, observer: INotificationObserver):
        self._observers.append(observer)
    
    def detach_observer(self, observer: INotificationObserver):
        self._observers.remove(observer)
    
    def _notify_observers(self, notification_data: dict):
        for observer in self._observers:
            observer.update(notification_data)
    
    def process_order(self, order_data: dict, notification_types: list):
        order_id = order_data['order_id']
        customer = order_data['customer']
        total = order_data['total']
        
        print(f"\n{'='*50}")
        print(f"Procesando pedido #{order_id}")
        print(f"Cliente: {customer['name']}")
        print(f"Total: ${total}")
        print(f"{'='*50}\n")
        
        print("🔍 Validando pedido...")
        if not self._validator_chain.validate(order_data):
            print("❌ Pedido inválido\n")
            return
        
        for notif_type in notification_types:
            try:
                notifier = self.factory.get_notifier(notif_type)
                notification_data = notifier.send(customer, order_id, total)
                self.logger.log(notification_data)
                self._notify_observers(notification_data)
            except ValueError as e:
                print(f"⚠️ Error: {e}\n")
    
    def get_notification_history(self):
        return self.logger.get_history()

# ========== CÓDIGO DE PRUEBA ==========
if __name__ == "__main__":
    print("=" * 70)
    print("DEMOSTRACIÓN PATRONES DE DISEÑO - NOTIFICACIONES")
    print("=" * 70)
    
    # SINGLETON
    print("\n🔷 SINGLETON")
    config1 = NotificationConfig()
    config2 = NotificationConfig()
    print(f"Misma instancia: {config1 is config2}")
    print(f"Config: {config1.get_config()}")
    
    # BUILDER
    print("\n🔷 BUILDER")
    order_premium = (OrderBuilder()
        .with_order_id('ORD-001')
        .with_customer('Ana García', 'ana@email.com', '+34-600-123-456', 'DEV-123')
        .with_total(150.50)
        .add_item('Laptop', 899.99, 1)
        .build())
    
    print(f"Pedido: {order_premium['order_id']}, Cliente: {order_premium['customer']['name']}, Total: ${order_premium['total']}")
    
    # Sistema principal
    system = OrderNotificationSystem()
    
    # OBSERVER
    analytics = AnalyticsObserver()
    audit = AuditObserver()
    system.attach_observer(analytics)
    system.attach_observer(audit)
    
    # DECORATOR
    print("\n🔷 DECORATOR")
    email_enhanced = LoggingDecorator(RetryDecorator(EmailNotifier(), 2))
    system.factory.register_notifier('email_enhanced', email_enhanced)
    
    # COMPOSITE
    print("\n🔷 COMPOSITE")
    premium_group = CompositeNotifier('Premium')
    premium_group.add(EmailNotifier())
    premium_group.add(SMSNotifier())
    premium_group.add(PushNotifier())
    system.factory.register_notifier('premium', premium_group)
    
    # OBSERVER + CHAIN OF RESPONSIBILITY
    print("\n🔷 OBSERVER + CHAIN OF RESPONSIBILITY")
    print("=" * 70)
    
    system.process_order({
        'order_id': 'ORD-001',
        'customer': {
            'name': 'Ana García',
            'email': 'ana@email.com',
            'phone': '+34-600-123-456',
            'device_id': 'DEV-123'
        },
        'total': 150.50
    }, ['premium'])
    
    system.process_order({
        'order_id': 'ORD-002',
        'customer': {
            'name': 'Carlos Ruiz',
            'email': 'carlos@email.com',
            'phone': '+34-600-789-012',
            'device_id': 'DEV-XYZ'
        },
        'total': 75.00
    }, ['email_enhanced'])
    
    # CHAIN (Validación Fallida)
    print("\n🔷 CHAIN (Validación Fallida)")
    print("-" * 50)
    system.process_order({
        'order_id': '',
        'customer': {'name': 'Pedro', 'email': 'pedro@email.com'},
        'total': -10
    }, ['email'])
    
    # ANALYTICS
    print("\n" + "=" * 70)
    print("📊 ANALYTICS")
    print("=" * 70)
    print(json.dumps(analytics.get_stats(), indent=2))
    
    # AUDITORÍA
    print("\n" + "=" * 70)
    print("🔍 AUDITORÍA")
    print("=" * 70)
    for entry in audit.audit_log:
        print(f"  {entry['timestamp']} | {entry['notification_type']} → {entry['recipient']}")
    
    # TOTAL
    print(f"\n{'='*70}")
    print(f"Total notificaciones: {len(system.get_notification_history())}")
    print(f"{'='*70}")