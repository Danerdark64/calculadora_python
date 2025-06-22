import tkinter as tk  # Importa la biblioteca Tkinter para crear la interfaz gráfica
from tkinter import ttk, messagebox  # Importa ttk para widgets mejorados y messagebox para mostrar mensajes de error

# Función para convertir un número entero a su representación binaria
def entero_a_binario(numero):
    if numero == 0:
        return '0'  # Si el número es 0, retorna '0'
    binario = ''
    # Mientras el número sea mayor que 0, se obtiene el residuo
    while numero > 0:
        residuo = numero % 2
        # Se construye la representación binaria
        binario = ('1' if residuo == 1 else '0') + binario
        numero = numero // 2  # División entera por 2
    return binario

# Función para convertir una cadena binaria a su representación entera
def binario_a_entero(binario):
    return int(binario, 2)  # Convierte la cadena binaria a entero usando base 2

# Función para convertir un número decimal (entero y fraccionario) a binario
def decimal_a_binario(numero, precision=4):
    parte_entera = int(numero)  # Separa la parte entera
    bin_entero = entero_a_binario(parte_entera)  # Convierte la parte entera a binario
    
    parte_fraccionaria = numero - parte_entera  # Calcula la parte fraccionaria
    bin_fraccion = ''
    # Convierte la parte fraccionaria a binario con la precisión especificada
    while precision > 0 and parte_fraccionaria != 0:
        parte_fraccionaria *= 2  # Multiplica la fracción por 2
        bit = int(parte_fraccionaria)  # Obtiene el bit
        bin_fraccion += str(bit)  # Agrega el bit a la representación binaria
        if bit == 1:
            parte_fraccionaria -= bit  # Resta 1 si el bit es 1
        precision -= 1  # Disminuye la precisión
    
    return f"{bin_entero}.{bin_fraccion}" if bin_fraccion else bin_entero  # Retorna el binario completo

# Función para convertir un número binario (con fracción) a decimal
def binario_a_decimal(binario):
    if '.' in binario:
        parte_entera, parte_fraccionaria = binario.split('.')  # Separa la parte entera y fraccionaria
    else:
        parte_entera, parte_fraccionaria = binario, ''  # Si no hay fracción, la parte fraccionaria es vacía
    
    decimal = int(parte_entera, 2)  # Convierte la parte entera a decimal
    exponente = -1  # Exponentes negativos para la parte fraccionaria
    # Convierte la parte fraccionaria manualmente
    for bit in parte_fraccionaria:
        decimal += int(bit) * (2 ** exponente)  # Suma el valor correspondiente
        exponente -= 1  # Disminuye el exponente
    return decimal  # Retorna el valor decimal total

# Función para sumar dos números en complemento a 2
def suma_binaria_comp2(num1, num2):
    return entero_a_binario(num1 + num2)  # Convierte la suma a binario

# Función para restar dos números en complemento a 2
def resta_binaria_comp2(num1, num2):
    resta = num1 - num2  # Realiza la resta
    if resta >= 0:
        return entero_a_binario(resta)  # Si la resta es positiva, convierte a binario
    else:
        # Para números negativos, se obtiene el complemento a 1
        complemento1 = ''.join(['1' if bit == '0' else '0' for bit in entero_a_binario(abs(resta))])
        # Luego se suma 1 para obtener el complemento a 2
        complemento2 = bin(int(complemento1, 2) + 1)[2:]
        return complemento2  # Retorna el complemento a 2

# Clase para la interfaz gráfica de la calculadora
class CalculadoraBinariaApp:
    def __init__(self, root):
        self.root = root  # Guarda la referencia a la ventana principal
        self.root.title("Calculadora Binaria Avanzada")  # Título de la ventana
        self.root.geometry("500x400")  # Tamaño de la ventana
        
        self.crear_widgets()  # Llama a la función para crear los widgets
    
    def crear_widgets(self):
        # Etiqueta del título
        ttk.Label(self.root, text="Calculadora Binaria", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Panel de selección de operación
        self.operacion = tk.StringVar()  # Variable para almacenar la operación seleccionada
        opciones = [
            "Entero a Binario", 
            "Binario a Entero",
            "Decimal a Binario",
            "Binario a Decimal",
            "Suma Binaria (C2)",
            "Resta Binaria (C2)"
        ]
        # Menú desplegable para seleccionar la operación
        ttk.OptionMenu(self.root, self.operacion, opciones[0], *opciones).pack(pady=5)
        
        # Campos de entrada
        self.frame_entrada = ttk.Frame(self.root)  # Crea un marco para los campos de entrada
        self.frame_entrada.pack(pady=10)
        
        # Etiqueta y campo de entrada para el primer valor
        ttk.Label(self.frame_entrada, text="Valor 1:").grid(row=0, column=0, padx=5)
        self.entrada1 = ttk.Entry(self.frame_entrada)  # Campo de entrada para el primer valor
        self.entrada1.grid(row=0, column=1, padx=5)
        
        # Etiqueta y campo de entrada para el segundo valor
        ttk.Label(self.frame_entrada, text="Valor 2:").grid(row=1, column=0, padx=5)
        self.entrada2 = ttk.Entry(self.frame_entrada)  # Campo de entrada para el segundo valor
        self.entrada2.grid(row=1, column=1, padx=5)
        self.entrada2.config(state="disabled")  # Inicialmente deshabilitado
        
        # Botón para realizar el cálculo
        ttk.Button(self.root, text="Calcular", command=self.calcular).pack(pady=10)
        
        # Área de resultados
        self.resultado = tk.Text(self.root, height=5, width=50, state="disabled")  # Área de texto para mostrar resultados
        self.resultado.pack(pady=10)
        
        # Eventos
        self.operacion.trace_add("write", self.actualizar_campos)  # Actualiza campos al cambiar la operación
    
    def actualizar_campos(self, *args):
        op = self.operacion.get()  # Obtiene la operación seleccionada
        # Habilita o deshabilita el segundo campo de entrada según la operación
        self.entrada2.config(state="normal" if op in ["Suma Binaria (C2)", "Resta Binaria (C2)"] else "disabled")
        self.limpiar_resultado()  # Limpia el área de resultados
    
    def calcular(self):
        try:
            op = self.operacion.get()  # Obtiene la operación seleccionada
            val1 = self.entrada1.get()  # Obtiene el primer valor
            
            # Realiza la conversión según la operación seleccionada
            if op == "Entero a Binario":
                res = entero_a_binario(int(val1))  # Convierte el entero a binario
                self.mostrar_resultado(f"Entero: {val1}\nBinario: {res}")
                
            elif op == "Binario a Entero":
                res = binario_a_entero(val1)  # Convierte el binario a entero
                self.mostrar_resultado(f"Binario: {val1}\nEntero: {res}")
                
            elif op == "Decimal a Binario":
                res = decimal_a_binario(float(val1))  # Convierte el decimal a binario
                self.mostrar_resultado(f"Decimal: {val1}\nBinario: {res}")
                
            elif op == "Binario a Decimal":
                res = binario_a_decimal(val1)  # Convierte el binario a decimal
                self.mostrar_resultado(f"Binario: {val1}\nDecimal: {res}")
                
            elif op in ["Suma Binaria (C2)", "Resta Binaria (C2)"]:
                val2 = self.entrada2.get()  # Obtiene el segundo valor
                # Convierte los valores según la operación
                num1 = int(val1) if op == "Suma Binaria (C2)" else binario_a_entero(val1)
                num2 = int(val2) if op == "Suma Binaria (C2)" else binario_a_entero(val2)
                
                if op == "Suma Binaria (C2)":
                    res = suma_binaria_comp2(num1, num2)  # Realiza la suma
                    self.mostrar_resultado(f"{entero_a_binario(num1)} + {entero_a_binario(num2)} = {res}")
                else:
                    res = resta_binaria_comp2(num1, num2)  # Realiza la resta
                    self.mostrar_resultado(f"{entero_a_binario(num1)} - {entero_a_binario(num2)} = {res}")
        
        except ValueError as e:
            messagebox.showerror("Error", f"Dato inválido: {e}")  # Muestra un mensaje de error si hay un problema con la entrada
    
    def mostrar_resultado(self, texto):
        self.resultado.config(state="normal")  # Habilita el área de resultados
        self.resultado.delete(1.0, tk.END)  # Limpia el área de resultados
        self.resultado.insert(tk.END, texto)  # Inserta el nuevo resultado
        self.resultado.config(state="disabled")  # Deshabilita el área de resultados
    
    def limpiar_resultado(self):
        self.resultado.config(state="normal")  # Habilita el área de resultados
        self.resultado.delete(1.0, tk.END)  # Limpia el área de resultados
        self.resultado.config(state="disabled")  # Deshabilita el área de resultados

# Punto de entrada principal del programa
if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal
    app = CalculadoraBinariaApp(root)  # Crea una instancia de la calculadora
    root.mainloop()  # Inicia el bucle principal de la interfaz gráfica