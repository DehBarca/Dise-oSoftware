from datetime import datetime
import json
from abc import ABC, abstractmethod
import copy

# ========== INTERFACES ==========
class IReportGenerator(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        pass
    
    @abstractmethod
    def get_report_type(self) -> str:
        pass


class IReportFormatter(ABC):
    @abstractmethod
    def format(self, content: str) -> str:
        pass
    
    @abstractmethod
    def get_format_type(self) -> str:
        pass


class IDeliveryMethod(ABC):
    @abstractmethod
    def deliver(self, report: str, report_type: str, format_type: str):
        pass
    
    @abstractmethod
    def get_delivery_type(self) -> str:
        pass

# ========== GENERADORES (SOLID: S, O, L, D) ==========
class SalesReportGenerator(IReportGenerator):
    def generate(self, data: dict) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_sales = sum(item["amount"] for item in data["sales"])
        
        content = f"{'='*60}\n"
        content += "           REPORTE DE VENTAS\n"
        content += f"{'='*60}\n"
        content += f"Fecha: {timestamp}\n\n"
        content += f"Total: ${total_sales:.2f}\n"
        content += f"Transacciones: {len(data['sales'])}\n"
        content += f"Periodo: {data['period']}\n\n"
        content += f"Detalle:\n{'-'*60}\n"
        
        for sale in data["sales"]:
            content += f"  • {sale['product']} - ${sale['amount']:.2f}\n"
        
        return content
    
    def get_report_type(self) -> str:
        return "sales"

class InventoryReportGenerator(IReportGenerator):
    def generate(self, data: dict) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_items = sum(item["quantity"] for item in data["items"])
        
        content = f"{'='*60}\n"
        content += "           REPORTE DE INVENTARIO\n"
        content += f"{'='*60}\n"
        content += f"Fecha: {timestamp}\n\n"
        content += f"Total: {total_items}\n"
        content += f"Categorías: {len(set(item['category'] for item in data['items']))}\n\n"
        content += f"Inventario:\n{'-'*60}\n"
        
        for item in data["items"]:
            content += f"  • {item['name']} ({item['category']}): {item['quantity']} uds\n"
        
        return content
    
    def get_report_type(self) -> str:
        return "inventory"

class FinancialReportGenerator(IReportGenerator):
    def generate(self, data: dict) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        balance = data['income'] - data['expenses']
        
        content = f"{'='*60}\n"
        content += "           REPORTE FINANCIERO\n"
        content += f"{'='*60}\n"
        content += f"Fecha: {timestamp}\n\n"
        content += f"Ingresos: ${data['income']:.2f}\n"
        content += f"Gastos: ${data['expenses']:.2f}\n"
        content += f"Balance: ${balance:.2f}\n"
        
        return content
    
    def get_report_type(self) -> str:
        return "financial"

# ========== FORMATEADORES ==========
class PDFFormatter(IReportFormatter):
    def format(self, content: str) -> str:
        print("📄 Formateando a PDF...")
        return f"[PDF FORMAT]\n{content}\n[END PDF]"
    
    def get_format_type(self) -> str:
        return "pdf"


class ExcelFormatter(IReportFormatter):
    def format(self, content: str) -> str:
        print("📊 Formateando a Excel...")
        return f"[EXCEL FORMAT]\n{content}\n[END EXCEL]"
    
    def get_format_type(self) -> str:
        return "excel"


class HTMLFormatter(IReportFormatter):
    def format(self, content: str) -> str:
        print("🌐 Formateando a HTML...")
        return f"<html><body><pre>{content}</pre></body></html>"
    
    def get_format_type(self) -> str:
        return "html"

# ========== MÉTODOS DE ENTREGA ==========
class EmailDelivery(IDeliveryMethod):
    def deliver(self, report: str, report_type: str, format_type: str):
        print("📧 Enviando por email a admin@company.com")
    
    def get_delivery_type(self) -> str:
        return "email"


class DownloadDelivery(IDeliveryMethod):
    def deliver(self, report: str, report_type: str, format_type: str):
        filename = f"report_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type}"
        print(f"💾 Guardando como: {filename}")
    
    def get_delivery_type(self) -> str:
        return "download"


class CloudDelivery(IDeliveryMethod):
    def deliver(self, report: str, report_type: str, format_type: str):
        url = f"https://cloud.company.com/reports/{report_type}"
        print(f"☁️ Subiendo a la nube: {url}")
    
    def get_delivery_type(self) -> str:
        return "cloud"

# ========== PATRÓN FACTORY (Creacional) ==========
class ReportGeneratorFactory:
    def __init__(self):
        self._generators = {
            'sales': SalesReportGenerator(),
            'inventory': InventoryReportGenerator(),
            'financial': FinancialReportGenerator()
        }
    
    def get_generator(self, report_type: str) -> IReportGenerator:
        generator = self._generators.get(report_type)
        if not generator:
            raise ValueError(f"Tipo no soportado: {report_type}")
        return generator


class ReportFormatterFactory:
    def __init__(self):
        self._formatters = {
            'pdf': PDFFormatter(),
            'excel': ExcelFormatter(),
            'html': HTMLFormatter()
        }
    
    def get_formatter(self, format_type: str) -> IReportFormatter:
        formatter = self._formatters.get(format_type)
        if not formatter:
            raise ValueError(f"Formato no soportado: {format_type}")
        return formatter


class DeliveryMethodFactory:
    def __init__(self):
        self._methods = {
            'email': EmailDelivery(),
            'download': DownloadDelivery(),
            'cloud': CloudDelivery()
        }
    
    def get_delivery_method(self, delivery_type: str) -> IDeliveryMethod:
        method = self._methods.get(delivery_type)
        if not method:
            raise ValueError(f"Entrega no soportada: {delivery_type}")
        return method

class ReportHistoryLogger:
    def __init__(self):
        self.reports_generated = []
    
    def log(self, report_type: str, format_type: str, delivery_type: str):
        self.reports_generated.append({
            "type": report_type,
            "format": format_type,
            "delivery": delivery_type,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def get_history(self) -> list:
        return self.reports_generated

# ========== PATRÓN BUILDER (Creacional) ==========
class ReportBuilder:
    def __init__(self):
        self._title = ""
        self._sections = []
        self._metadata = {}
        self._footer = ""
    
    def with_title(self, title: str):
        self._title = title
        return self
    
    def add_section(self, section_name: str, content: str):
        self._sections.append({'name': section_name, 'content': content})
        return self
    
    def with_metadata(self, author: str, department: str, confidential: bool = False):
        self._metadata = {
            'author': author,
            'department': department,
            'confidential': confidential,
            'generated_at': datetime.now().isoformat()
        }
        return self
    
    def with_footer(self, footer: str):
        self._footer = footer
        return self
    
    def build(self) -> str:
        report = f"{'='*70}\n"
        report += f"{self._title.center(70)}\n"
        report += f"{'='*70}\n\n"
        
        if self._metadata:
            report += f"Autor: {self._metadata.get('author', 'N/A')}\n"
            report += f"Departamento: {self._metadata.get('department', 'N/A')}\n"
            if self._metadata.get('confidential'):
                report += "⚠️ CONFIDENCIAL\n"
            report += f"Generado: {self._metadata.get('generated_at')}\n\n"
        
        for section in self._sections:
            report += f"\n{section['name']}\n"
            report += f"{'-'*70}\n"
            report += f"{section['content']}\n"
        
        if self._footer:
            report += f"\n{'='*70}\n"
            report += f"{self._footer}\n"
        
        return report

# ========== PATRÓN PROTOTYPE (Creacional) ==========
class Report:
    def __init__(self, report_type: str, data: dict, format_type: str):
        self.report_type = report_type
        self.data = data.copy()
        self.format_type = format_type
        self.metadata = {
            'created_at': datetime.now().isoformat(),
            'version': 1
        }
    
    def clone(self):
        cloned = copy.deepcopy(self)
        cloned.metadata['version'] = self.metadata['version'] + 1
        cloned.metadata['cloned_at'] = datetime.now().isoformat()
        print(f"   📋 Clonado: {self.report_type} (v{cloned.metadata['version']})")
        return cloned
    
    def __str__(self):
        return f"Report({self.report_type}, v{self.metadata['version']}, {self.format_type})"

# ========== PATRÓN ADAPTER (Estructural) ==========
class IDataSource(ABC):
    @abstractmethod
    def get_data(self) -> dict:
        pass


class LegacyDataSource:
    def fetch_legacy_data(self):
        return {
            'sales_info': [
                {'item': 'Laptop', 'price': 899.99, 'qty': 10},
                {'item': 'Mouse', 'price': 25.50, 'qty': 50}
            ],
            'time_period': 'Q1 2024'
        }


class DataSourceAdapter(IDataSource):
    def __init__(self, legacy_source: LegacyDataSource):
        self._legacy = legacy_source
    
    def get_data(self) -> dict:
        legacy_data = self._legacy.fetch_legacy_data()
        
        adapted_data = {
            'period': legacy_data['time_period'],
            'sales': [
                {
                    'product': item['item'],
                    'amount': item['price'] * item['qty']
                }
                for item in legacy_data['sales_info']
            ]
        }
        
        print("   🔄 Datos adaptados desde sistema legacy")
        return adapted_data

# ========== PATRÓN FACADE (Estructural) ==========
class ReportGenerationFacade:
    def __init__(self):
        self.system = ReportSystem()
    
    def generate_quick_sales_report(self, sales_data: dict):
        print("   🚀 Usando Facade para generación rápida...")
        return self.system.generate_report('sales', sales_data, 'pdf', 'email')
    
    def generate_inventory_report_for_download(self, inventory_data: dict):
        print("   🚀 Usando Facade para reporte de inventario...")
        return self.system.generate_report('inventory', inventory_data, 'excel', 'download')
    
    def generate_financial_summary(self, financial_data: dict):
        print("   🚀 Usando Facade para resumen financiero...")
        return self.system.generate_report('financial', financial_data, 'html', 'cloud')

# ========== PATRÓN TEMPLATE METHOD (Comportamiento) ==========
class ReportTemplate(ABC):
    def generate_full_report(self, data: dict) -> str:
        header = self._generate_header()
        content = self._generate_content(data)
        footer = self._generate_footer()
        return f"{header}\n{content}\n{footer}"
    
    def _generate_header(self) -> str:
        title = self.get_title()
        date = datetime.now().strftime('%Y-%m-%d')
        return f"{'='*60}\n{title.center(60)}\nFecha: {date}\n{'='*60}"
    
    @abstractmethod
    def get_title(self) -> str:
        pass
    
    @abstractmethod
    def _generate_content(self, data: dict) -> str:
        pass
    
    def _generate_footer(self) -> str:
        return f"{'='*60}\nGenerado automáticamente"


class DailySalesReport(ReportTemplate):
    def get_title(self) -> str:
        return "REPORTE DIARIO DE VENTAS"
    
    def _generate_content(self, data: dict) -> str:
        content = f"\nVentas del día:\n{'-'*60}\n"
        total = sum(s['amount'] for s in data['sales'])
        
        for sale in data['sales']:
            content += f"  • {sale['product']}: ${sale['amount']:.2f}\n"
        
        content += f"\n{'-'*60}\n"
        content += f"TOTAL: ${total:.2f}"
        
        return content

# ========== PATRÓN STRATEGY (Comportamiento) ==========
class IReportStrategy(ABC):
    @abstractmethod
    def execute(self, data: dict) -> str:
        pass


class DetailedStrategy(IReportStrategy):
    def execute(self, data: dict) -> str:
        content = "REPORTE DETALLADO\n"
        content += "=" * 60 + "\n"
        
        for key, value in data.items():
            content += f"{key}: {value}\n"
        
        return content


class SummaryStrategy(IReportStrategy):
    def execute(self, data: dict) -> str:
        first_key = list(data.keys())[0] if data else 'N/A'
        content = "RESUMEN\n"
        content += "=" * 60 + "\n"
        content += f"Total items: {len(data)}\n"
        content += f"Primer registro: {first_key}"
        return content


class ReportContext:
    def __init__(self, strategy: IReportStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: IReportStrategy):
        self._strategy = strategy
    
    def execute_strategy(self, data: dict) -> str:
        return self._strategy.execute(data)

# ========== SISTEMA PRINCIPAL ==========
class ReportSystem:
    def __init__(self,
                 generator_factory: ReportGeneratorFactory = None,
                 formatter_factory: ReportFormatterFactory = None,
                 delivery_factory: DeliveryMethodFactory = None,
                 logger: ReportHistoryLogger = None):
        self.generator_factory = generator_factory or ReportGeneratorFactory()
        self.formatter_factory = formatter_factory or ReportFormatterFactory()
        self.delivery_factory = delivery_factory or DeliveryMethodFactory()
        self.logger = logger or ReportHistoryLogger()
    
    def generate_report(self, report_type: str, data: dict, output_format: str, delivery_method: str):
        try:
            # Obtener componentes a través de las factories
            generator = self.generator_factory.get_generator(report_type)
            formatter = self.formatter_factory.get_formatter(output_format)
            delivery = self.delivery_factory.get_delivery_method(delivery_method)
            
            # Generar y formatear el reporte
            report_content = generator.generate(data)
            formatted_report = formatter.format(report_content)
            
            # Entregar el reporte
            delivery.deliver(formatted_report, report_type, output_format)
            
            # Registrar en el historial
            self.logger.log(report_type, output_format, delivery_method)
            
            print("\n✅ Reporte generado exitosamente\n")
            print(formatted_report)
            print("\n" + "=" * 60 + "\n")
            
            return formatted_report
            
        except ValueError as e:
            print(f"⚠️ Error: {e}\n")
            return None
    
    def get_report_history(self):
        return self.logger.get_history()

# ========== CÓDIGO DE PRUEBA ==========
if __name__ == "__main__":
    print("=" * 70)
    print("DEMOSTRACIÓN PATRONES DE DISEÑO - REPORTES")
    print("=" * 70)
    
    system = ReportSystem()
    
    # Datos de prueba
    print("\n🔷 FACTORIES + STRATEGY + TEMPLATE")
    sales_data = {
        'period': 'Enero 2024',
        'sales': [
            {'product': 'Laptop HP', 'amount': 899.99},
            {'product': 'Mouse', 'amount': 25.50}
        ]
    }
    inventory_data = {
        'items': [
            {'name': 'Laptop HP', 'category': 'Computadoras', 'quantity': 15},
            {'name': 'Mouse', 'category': 'Accesorios', 'quantity': 50}
        ]
    }
    financial_data = {
        'income': 50000.00,
        'expenses': 32000.00
    }
    
    system.generate_report('sales', sales_data, 'pdf', 'email')
    system.generate_report('inventory', inventory_data, 'excel', 'download')
    system.generate_report('financial', financial_data, 'html', 'cloud')
    
    print("\n🔷 BUILDER")
    builder = ReportBuilder()
    custom_report = (builder
        .with_title("REPORTE CUSTOM")
        .add_section("Sección 1", "Contenido aquí")
        .with_metadata("Juan Pérez", "Ventas", True)
        .with_footer("Confidencial")
        .build())
    print(custom_report)
    
    print("\n🔷 PROTOTYPE")
    original = Report('sales', sales_data, 'pdf')
    clone1 = original.clone()
    clone2 = original.clone()
    print(f"Original: {original}")
    print(f"Clon 1: {clone1}")
    print(f"Clon 2: {clone2}")
    
    print("\n🔷 ADAPTER")
    legacy = LegacyDataSource()
    adapter = DataSourceAdapter(legacy)
    adapted_data = adapter.get_data()
    print(f"Datos adaptados: {adapted_data['period']}, {len(adapted_data['sales'])} ventas")
    
    print("\n🔷 FACADE")
    facade = ReportGenerationFacade()
    facade.generate_quick_sales_report(sales_data)
    
    print("\n🔷 TEMPLATE METHOD")
    daily_report = DailySalesReport()
    print(daily_report.generate_full_report(sales_data))
    
    print("\n🔷 STRATEGY")
    context = ReportContext(DetailedStrategy())
    print(context.execute_strategy(sales_data))
    context.set_strategy(SummaryStrategy())
    print(context.execute_strategy(sales_data))
    
    print("\n" + "=" * 70)
    print("📊 HISTORIAL")
    print("=" * 70)
    print(json.dumps(system.get_report_history(), indent=2))

