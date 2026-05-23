import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 1. CONFIGURACIÓN DEL SISTEMA EMBAJADOR PREMIUM
st.set_page_config(
    page_title="PastaControl ERP Enterprise v3.0",
    page_icon="🍝",
    layout="wide"
)

# Estilos CSS avanzados (Colores profundos, diseño de documentos reales y animaciones)
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        color: white; padding: 30px; border-radius: 12px; text-align: center;
        margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border-bottom: 5px solid #F59E0B;
    }
    .main-header h1 { margin: 0; font-size: 34px; font-weight: 800; letter-spacing: 1px; }
    .main-header p { margin: 8px 0 0 0; font-size: 16px; opacity: 0.9; }
    
    .doc-box {
        background-color: #FFFFFF; border: 2px dashed #94A3B8;
        padding: 30px; border-radius: 8px; margin-top: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04); font-family: 'Courier New', Courier, monospace;
    }
    .doc-title { font-size: 22px; font-weight: bold; color: #0F172A; text-align: center; margin-bottom: 20px; text-transform: uppercase; border-bottom: 3px solid #0F172A; padding-bottom: 8px; }
    
    .card-paso { background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 18px; border-radius: 8px; margin-bottom: 15px; border-left: 6px solid #F59E0B; }
    .card-critico { border-left: 6px solid #B91C1C !important; background-color: #FEE2E2 !important; }
    .titulo-paso { font-size: 16px; font-weight: bold; color: #1E3A8A; }
    
    /* Botón de impresión ocultable */
    .print-btn-html {
        background-color: #10B981; color: white; padding: 10px 20px;
        border: none; border-radius: 6px; font-weight: bold; cursor: pointer;
        font-family: sans-serif; text-decoration: none; display: inline-block;
    }
    .print-btn-html:hover { background-color: #059669; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-header">
        <h1>📊 PASTACONTROL ERP ENTERPRISE v3.0</h1>
        <p>Plataforma de Simulación Industrial Completa: Módulos Comerciales, Financieros y de Aseguramiento de Calidad</p>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# INICIALIZACIÓN DE LA BASE DE DATOS EN MEMORIA
# ==============================================================================
if 'historial_pedidos' not in st.session_state:
    st.session_state['historial_pedidos'] = []

# Parámetros fijos de ingeniería del proyecto
porcentajes = {"Yuca": 0.40, "Caupí": 0.15, "Auyama": 0.15, "Agua": 0.25, "Huevo": 0.05}
precios_proveedor = {"Yuca": 4500, "Caupí": 6000, "Auyama": 3500, "Agua": 100, "Huevo": 8000}

# ==============================================================================
# PANEL DE CONTROL GENERAL (DASHBOARD GLOBAL DE LA COMPAÑÍA)
# ==============================================================================
st.markdown("### 📈 Panel de Control de la Compañía (KPIs Globales)")
if len(st.session_state['historial_pedidos']) == 0:
    st.info("💡 El sistema está listo. Registre su primer pedido en la Pestaña 1 para inicializar el flujo industrial.")
else:
    total_kilos_global = sum(p['kilos'] for p in st.session_state['historial_pedidos'])
    total_ventas_global = sum(p['total_dinero'] for p in st.session_state['historial_pedidos'])
    total_costos_global = sum(p['costo_materias'] for p in st.session_state['historial_pedidos'])
    total_energia_global = sum(p['costo_energia'] for p in st.session_state['historial_pedidos'])
    
    # Costo total acumulado incluyendo servicios públicos
    costo_operativo_total = total_costos_global + total_energia_global
    total_utilidad_global = total_ventas_global - costo_operativo_total
    
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    col_g1.metric(label="📦 Órdenes en Cola", value=f"{len(st.session_state['historial_pedidos'])} pedidos")
    col_g2.metric(label="🌾 Masa a Fabricar", value=f"{total_kilos_global:,.0f} kg")
    col_g3.metric(label="💰 Ventas Brutas", value=f"${total_ventas_global:,.0f}")
    col_g4.metric(label="🎯 Utilidad Neta Real", value=f"${total_utilidad_global:,.0f}", delta=f"{((total_utilidad_global/total_ventas_global)*100):.1f}% Margen")

st.markdown("---")

# ==============================================================================
# SISTEMA DE PESTAÑAS (FLUJO INTEGRADO DE OPERACIÓN)
# ==============================================================================
pestana_comercial, pestana_historial, pestana_planta, pestana_calidad = st.tabs([
    "📥 1. Entrada de Pedidos (Venta)",
    "📋 2. Historial de Órdenes Guardadas",
    "🏭 3. Plan de Planta y Abastecimiento",
    "🔬 4. Laboratorio de Calidad (Control NTC 267)"
])

# ------------------------------------------------------------------------------
# PESTAÑA 1: ENTRADA DE PEDIDOS (MÓDULO COMERCIAL)
# ------------------------------------------------------------------------------
with pestana_comercial:
    st.markdown("#### 👤 Datos de la Nueva Orden de Venta")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        cliente = st.text_input("Nombre de la Empresa / Cliente:", value="Distribuidora NutriVida")
        nit_cliente = st.text_input("Identificación / NIT:", value="900.341.255-1")
    with col_r2:
        kilos = st.number_input("Cantidad de Pasta a Fabricar (Kilos):", min_value=5, max_value=10000, value=100, step=5)
        precio_kg = st.number_input("Precio Pactado por Kilo ($ COP):", min_value=5000, value=15000, step=500)
        
    # IDEA 4: SIMULACIÓN DE CONSUMO ENERGÉTICO (Servicios Públicos)
    # Valores base promedio: 0.12 kWh de energía por kg de pasta y 0.05 m3 de gas para cocción/secado
    costo_energia_orden = kilos * ((0.12 * 950) + (0.05 * 1400)) # tarifas estimadas COP
    subtotal_dinero = kilos * precio_kg
    costo_materia_orden = sum((kilos * porcentajes[ing] * precios_proveedor[ing]) for ing in porcentajes.keys())
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 REGISTRAR Y GUARDAR PEDIDO EN EL HISTORIAL"):
        nuevo_pedido = {
            "id": len(st.session_state['historial_pedidos']) + 1,
            "cliente": cliente,
            "nit": nit_cliente,
            "kilos": kilos,
            "precio_kg": precio_kg,
            "total_dinero": subtotal_dinero,
            "costo_materias": costo_materia_orden,
            "costo_energia": costo_energia_orden,
            "fecha": datetime.now().strftime('%d/%m/%Y %H:%M')
        }
        st.session_state['historial_pedidos'].append(nuevo_pedido)
        st.success(f"✅ ¡Pedido No. {nuevo_pedido['id']} guardado con éxito!")
        st.rerun()

    st.markdown("---")
    st.markdown("#### 📄 Vista Previa del Documento Comercial")
    
    # IDEA 1: BOTÓN DE IMPRESIÓN / DESCARGA PDF INTEGRADO EN HTML
    html_remision = f"""
    <div class="doc-box" id="seccion-remision">
        <div style="text-align: right; margin-bottom: 10px;">
            <button onclick="window.print()" class="print-btn-html">🖨️ Generar PDF / Imprimir Documento</button>
        </div>
        <div class="doc-title">Remisión Oficial de Entrega No. RM-2026-001</div>
        <table style="width:100%; font-size:14px; border-collapse: collapse;">
            <tr><td><strong>Cliente:</strong> {cliente}</td><td style="text-align:right;"><strong>NIT:</strong> {nit_cliente}</td></tr>
            <tr><td><strong>Fecha de Proceso:</strong> {datetime.now().strftime('%d/%m/%Y')}</td><td style="text-align:right;"><strong>Ubicación:</strong> Planta Central</td></tr>
            <tr style="border-bottom: 2px solid #000; border-top: 2px solid #000;"><td style="padding:10px 0;"><strong>Detalle del Ítem Despachado</strong></td><td style="text-align:right; padding:10px 0;"><strong>Subtotal</strong></td></tr>
            <tr><td style="padding:8px 0;">Pasta Alimenticia Funcional Libre de Gluten (Fórmula Estándar F1)<br><small>{kilos:,.0f} kg netos @ ${precio_kg:,.0f}/kg</small></td><td style="text-align:right; vertical-align:top; padding:8px 0;">${subtotal_dinero:,.0f}</td></tr>
            <tr style="border-top: 2px solid #000; font-weight:bold;"><td style="padding:10px 0;">VALOR TOTAL FACTURADO:</td><td style="text-align:right; padding:10px 0; font-size:16px;">${subtotal_dinero:,.0f} COP</td></tr>
        </table>
    </div>
    """
    st.markdown(html_remision, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PESTAÑA 2: HISTORIAL DE ÓRDENES GUARDADAS
# ------------------------------------------------------------------------------
with pestana_historial:
    st.markdown("#### 📂 Libro General de Órdenes del Turno")
    if len(st.session_state['historial_pedidos']) == 0:
        st.warning("No hay órdenes guardadas en la memoria activa del sistema.")
    else:
        raw_df = pd.DataFrame(st.session_state['historial_pedidos'])
        df_visual = pd.DataFrame({
            "No. Orden": raw_df["id"],
            "Fecha Registro": raw_df["fecha"],
            "Cliente / Distribuidor": raw_df["cliente"],
            "Volumen Solicitado": raw_df["kilos"].apply(lambda x: f"{x:,.0f} kg"),
            "Valor Bruto": raw_df["total_dinero"].apply(lambda x: f"${x:,.0f}"),
            "Costo Materia Prima": raw_df["costo_materias"].apply(lambda x: f"${x:,.0f}"),
            "Gasto Energético Est.": raw_df["costo_energia"].apply(lambda x: f"${x:,.0f}")
        })
        st.dataframe(df_visual, width="stretch", hide_index=True)
        
        if st.button("🗑️ Reiniciar / Vaciar Todo el Historial"):
            st.session_state['historial_pedidos'] = []
            st.rerun()

# ------------------------------------------------------------------------------
# PESTAÑA 3: PLAN DE PLANTA E INSUMOS CONSOLIDADOS (ÁREA INDUSTRIAL)
# ------------------------------------------------------------------------------
with pestana_planta:
    if len(st.session_state['historial_pedidos']) == 0:
        st.warning("Ingrese pedidos en la primera pestaña para activar el Plan Maestro de Producción.")
    else:
        kilos_totales_acumulados = sum(p['kilos'] for p in st.session_state['historial_pedidos'])
        costos_totales_energia = sum(p['costo_energia'] for p in st.session_state['historial_pedidos'])
        
        st.markdown(f"### 🥣 Plan Maestro de Producción Consolidado: **{kilos_totales_acumulados:,.0f} Kilos Totales**")
        
        col_p1, col_p2 = st.columns([2, 1])
        
        with col_p1:
            st.write("Cantidad neta de materia prima que el supervisor de bodega debe despachar a los operarios:")
            insumos_totales_kg = [kilos_totales_acumulados * pct for pct in porcentajes.values()]
            costos_totales_insumos = [insumos_totales_kg[i] * list(precios_proveedor.values())[i] for i in range(len(insumos_totales_kg))]
            
            df_consolidado = pd.DataFrame({
                "Materia Prima Requerida": ["Harina de Yuca Industrial", "Harina de Caupí (Frijol)", "Harina de Auyama Deshidratada", "Suministro de Agua Potable", "Huevo Líquido Pasteurizado"],
                "Porcentaje Fórmula": [f"{p*100:.1f}%" for p in porcentajes.values()],
                "Masa Total a Pesar": [f"{k:,.1f} kg" for k in insumos_totales_kg],
                "Presupuesto de Gasto": [f"${c:,.0f} COP" for c in costos_totales_insumos]
            })
            st.dataframe(df_consolidado, width="stretch", hide_index=True)
            
            # IDEA 4 EXPLICADA: Desglose de servicios públicos
            st.markdown("##### ⚡ Detalle del Consumo de Servicios Públicos Proyectado:")
            st.markdown(f"""
            *   **Consumo Eléctrico Estimado (Extrusor y Bandas):** ${(costos_totales_energia*0.6):,.0f} COP
            *   **Consumo Térmico Estimado (Gas en Cocción y Túnel):** ${(costos_totales_energia*0.4):,.0f} COP
            """)
            
        with col_p2:
            # IDEA 3: GRÁFICO DE TORTA DINÁMICO PARA EL ALMACÉN
            st.markdown("##### 🥧 Distribución de Peso en Tolva")
            fig, ax = plt.subplots(figsize=(4.5, 4.5))
            labels = ['Yuca', 'Caupí', 'Auyama', 'Agua', 'Huevo']
            colors_pie = ["#1E3A8A", "#2563EB", "#F59E0B", "#94A3B8", "#CBD5E1"]
            
            ax.pie(insumos_totales_kg, labels=labels, autopct='%1.0f%%', startangle=90, colors=colors_pie, textprops={'fontweight':'bold', 'fontsize':10})
            ax.axis('equal')
            plt.tight_layout()
            st.pyplot(fig)

        st.markdown("---")
        st.markdown("#### 🏭 Instrucciones Operativas de Flujo (Límites de Merma)")
        st.markdown(f"""
        <div class="card-paso">
            <div class="titulo-paso">🟢 Paso 1: Adecuación e Inspección Fitosanitaria</div>
            <p style="margin:2px 0 0 0; font-size:14px; color:#334155;">Seleccionar y lavar. <strong>Merma máxima tolerada para este volumen acumulado:</strong> Selección ({(kilos_totales_acumulados*0.05):.1f} kg) y Lavado ({(kilos_totales_acumulados*0.08):.1f} kg).</p>
        </div>
        <div class="card-paso">
            <div class="titulo-paso">🔥 Paso 2: Tratamiento Térmico Operativo</div>
            <p style="margin:2px 0 0 0; font-size:14px; color:#334155;">Cocción controlada de almidones estructurales nativos. Rango térmico obligatorio: <strong>65°C a 80°C</strong>.</p>
        </div>
        <div class="card-paso card-critico">
            <div class="titulo-paso" style="color:#991B1B;">🚨 Paso 3: Mezclado Mecánico y Extrusión (Núcleo del Proceso)</div>
            <p style="margin:2px 0 0 0; font-size:14px; color:#7F1D1D;">Cargar las cantidades de la tabla. El aporte de Harina de Caupí ({insumos_totales_kg[1]:.1f} kg) garantiza el porcentaje de proteína requerido para dar fuerza elástica a la masa ante el descarte del gluten.</p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PESTAÑA 4: LABORATORIO DE CALIDAD (IDEA 2: GRÁFICOS DE SEMÁFORO Y ADVERTENCIAS)
# ------------------------------------------------------------------------------
with pestana_calidad:
    st.markdown("### 🔬 Módulo de Aseguramiento de Calidad en Línea")
    st.write("Simulador de control de lotes para el cumplimiento de la Norma Técnica Colombiana **NTC 267** (Humedad estándar para pastas alimenticias).")
    
    st.markdown("#### 🎚️ Registro de Mediciones del Operario de Calidad")
    humedad_ingresada = st.slider(
        "Indique el % de humedad registrado por el higrómetro al salir del túnel de secado (Etapa 4):",
        min_value=2.0, max_value=10.0, value=4.5, step=0.1
    )
    
    st.markdown("---")
    st.markdown("#### 🚦 Estado de Aprobación de Inocuidad (Semáforo Dinámico)")
    
    # Lógica del semáforo dinámico de calidad
    if humedad_ingresada <= 5.0:
        # Estado Verde - Cumple Norma
        st.success(f"🟢 **LOTE APROBADO** | Humedad registrada: {humedad_ingresada:.1f}%. Cumple estrictamente con el requerimiento normativo de la **NTC 267** (Máximo 5.0% de humedad). El lote puede pasar al área de empaque secundario.")
        
        # Dibujar indicador visual verde
        fig, ax = plt.subplots(figsize=(8, 0.8))
        ax.barh(["Humedad"], [humedad_ingresada], color='#10B981', edgecolor='#047857', height=0.5)
        ax.axvline(5.0, color='#B91C1C', linestyle='--', linewidth=2, label="Límite Máx NTC 267 (5%)")
        ax.set_xlim(0, 10)
        ax.legend(loc="upper right")
        st.pyplot(fig)
        
    elif 5.0 < humedad_ingresada <= 6.0:
        # Estado Amarillo - Alerta / Retrabajo
        st.warning(f"🟡 **LOTE EN REVISIÓN / PRECAUCIÓN** | Humedad registrada: {humedad_ingresada:.1f}%. Supera el límite de la norma **NTC 267**. **Acción correctiva inmediata:** Desviar el lote nuevamente al túnel de secado por 15 minutos adicionales antes de autorizar el sellado.")
        
        # Dibujar indicador visual amarillo
        fig, ax = plt.subplots(figsize=(8, 0.8))
        ax.barh(["Humedad"], [humedad_ingresada], color='#F59E0B', edgecolor='#B45309', height=0.5)
        ax.axvline(5.0, color='#B91C1C', linestyle='--', linewidth=2, label="Límite Máx NTC 267 (5%)")
        ax.set_xlim(0, 10)
        ax.legend(loc="upper right")
        st.pyplot(fig)
        
    else:
        # Estado Rojo - Rechazado
        st.error(f"🔴 **LOTE RECHAZADO / MERMA** | Humedad crítica detectada: {humedad_ingresada:.1f}%. El producto retiene demasiada agua libre, lo que compromete la vida útil y promueve el desarrollo de mohos y levaduras. El lote queda bloqueado por el departamento de calidad.")
        
        # Dibujar indicador visual rojo
        fig, ax = plt.subplots(figsize=(8, 0.8))
        ax.barh(["Humedad"], [humedad_ingresada], color='#EF4444', edgecolor='#B91C1C', height=0.5)
        ax.axvline(5.0, color='#B91C1C', linestyle='--', linewidth=2, label="Límite Máx NTC 267 (5%)")
        ax.set_xlim(0, 10)
        ax.legend(loc="upper right")
        st.pyplot(fig)

# Pie de página final blindado
st.markdown("---")
st.caption("🔒 PastaControl Enterprise System • Versión de Alta Fidelidad para Sustentación Pública • Derechos Reservados")