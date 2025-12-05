import pandas as pd
import numpy as np




df = pd.read_csv("ventas.csv")



columnas_numericas = ['Cantidad', 'PrecioUnitario', 'Total']

for col in columnas_numericas:
  
    df[col] = pd.to_numeric(df[col], errors='coerce')

    promedio = df[col].mean()
    df[col].fillna(promedio, inplace=True)



df['Subtotal_Calculado'] = df['Cantidad'] * df['PrecioUnitario']


df['Diferencia_Absoluta'] = abs(df['Subtotal_Calculado'].round(2) - df['Total'].round(2))


UMBRAL_FLOTANTE = 1e-6 

df['Error_Relativo'] = np.where(
    
    abs(df['Total']) > UMBRAL_FLOTANTE,
    
    df['Diferencia_Absoluta'] / abs(df['Total']),
   
    np.inf
)


UMBRAL_ERROR = 0.05
df['Es_Inconsistente'] = df['Error_Relativo'] > UMBRAL_ERROR


df_inconsistencias = df[df['Es_Inconsistente']].copy()



df_inconsistencias_export = df_inconsistencias[[
    'Fecha', 'Cliente', 'Producto', 'Cantidad', 'PrecioUnitario', 'Total',
    'Subtotal_Calculado', 'Diferencia_Absoluta', 'Error_Relativo'
]].copy()
df_inconsistencias_export.to_csv("inconsistencias.csv", index=False)



total_inconsistente = len(df_inconsistencias)


promedio_error_relativo = df_inconsistencias['Error_Relativo'].mean() if total_inconsistente > 0 else 0


if total_inconsistente > 0:
 
    producto_mas_inconsistente = df_inconsistencias['Producto'].mode().iloc[0]
else:
    producto_mas_inconsistente = "N/A (No hay inconsistencias)"

print(f"Total de registros inconsistentes: {total_inconsistente}")
print(f"Promedio del error relativo: {promedio_error_relativo:.4f}")
print(f"Producto con más inconsistencias: {producto_mas_inconsistente}")


print("\nPrimeros 5 registros inconsistentes exportados (muestra):")
print(df_inconsistencias_export.head(5).to_string(index=False))