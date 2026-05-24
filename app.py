import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 1. CONFIGURACIÓN DEL SISTEMA ENTERPRISE v7.1
st.set_page_config(
    page_title="PastaControl ERP v7.1",
    page_icon="🍝",
    layout="wide"
)

# Estilos CSS corregidos con colores de texto negro profundo para alta visibilidad
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        color: white !important; padding: 30px; border-radius: 12px; text-align: center;
        margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border-bottom: 5px solid #F59E0B;
    }
    .main-header h1 { color: white !important; margin: 0; font-size: 34px; font-weight: 800; letter-spacing: 1px; }
    .main-header p { color: white !important; margin: 8px 0 0 0; font-size: 16px; opacity: 0.9; }
    
    /* Caja del documento obligatoriamente blanca con textos negros muy fuertes */
    .doc-box {
        background-color: #FFFFFF !important; border: 2px dashed #94A3B8;
        padding: 40px; border-radius: 10px; margin-top: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04); max-width: 800px; margin-left: auto; margin-right: auto;
        color: #000000 !important;
    }
    .doc-title { font-size: 24px; font-weight: bold; color: #1E3A8A !important; text-align: center; margin-bottom: 25px; text-transform: uppercase; border-bottom: 3px solid #1E3A8A; padding-bottom: 10px; letter-spacing: 1px; }
    
    /* Forzar que todos los datos internos de la tabla y remisión sean negros legibles */
    .doc-box td, .doc-box tr, .doc-box strong, .doc-box small {
        color: #000000 !important;
    }
    
    .card-paso { background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 18px; border-radius: 8px; margin-bottom: 15px; border-left: 6px solid #F59E0B; }
    .card-critico { border-left: 6px solid #B91C1C !important; background-color: #FEE2E2 !important; }
    .titulo-paso { font-size: 16px; font-weight: bold; color: #1E3A8A; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-header">
        <h1>📊 PASTACONTROL ERP ENTERPRISE v7.1</h1>
        <p>Módulos Avanzados de Manufactura Agroindustrial y Gestión Financiera Comercial</p>
    </div>
""", unsafe_allow_html=True)

if 'historial_pedidos' not in st.session_state:
    st.session_state['historial_pedidos'] = []

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
    
    costo_operativo_total = total_costos_global + total_energia_global
    total_utilidad_global = total_ventas_global - costo_operativo_total
    
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    col_g1.metric(label="📦 Órdenes en Cola", value=f"{len(st.session_state['historial_pedidos'])} pedidos")
    col_g2.metric(label="🌾 Masa a Fabricar", value=f"{total_kilos_global:,.0f} kg")
    col_g3.metric(label="💰 Ventas Brutas", value=f"${total_ventas_global:,.0f}")
    col_g4.metric(label="🎯 Utilidad Neta Real", value=f"${total_utilidad_global:,.0f}", delta=f"{((total_utilidad_global/total_ventas_global)*100):.1f}% Margen")

st.markdown("---")

# ==============================================================================
# SISTEMA DE PESTAÑAS
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
        
    costo_energia_orden = kilos * ((0.12 * 950) + (0.05 * 1400))
    subtotal_dinero = kilos * precio_kg
    costo_materia_orden = sum((kilos * porcentajes[ing] * precios_proveedor[ing]) for ing in porcentajes.keys())
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 REGISTRAR Y GUARDAR PEDIDO EN EL HISTORIAL"):
        nuevo_pedido = {
            "id": len(st.session_state['historial_pedidos']) + 1,
            "fecha": datetime.now().strftime('%d/%m/%Y %H:%M'),
            "cliente": cliente,
            "nit": nit_cliente,
            "kilos": kilos,
            "precio_kg": precio_kg,
            "total_dinero": subtotal_dinero,
            "costo_materias": costo_materia_orden,
            "costo_energia": costo_energia_orden
        }
        st.session_state['historial_pedidos'].append(nuevo_pedido)
        st.success(f"✅ ¡Pedido No. {nuevo_pedido['id']} guardado con éxito!")
        st.rerun()

    st.markdown("---")
    st.markdown("#### 📄 Vista Previa del Documento Comercial")
    
    # Renderizado final con textos blindados en color negro puro
    html_remision = f"""
    <div class="doc-box">
        <div class="doc-title">REMISIÓN DE ENTREGA COMERCIAL</div>
        <div style="text-align: center; font-size: 12px; color: #334155; margin-bottom: 25px; font-family: sans-serif;">
            <strong>PASTACONTROL AGROINDUSTRIAL S.A.S.</strong><br>
            Nit: 901.888.234-0 • Planta de Procesamiento Central<br>
        </div>
        <table style="width:100%; font-size:14px; margin-top: 15px; margin-bottom: 25px; font-family: sans-serif; line-height: 20px;">
            <tr><td style="color: #000000 !important;"><strong>CLIENTE:</strong> {cliente}</td><td style="text-align:right; color: #000000 !important;"><strong>REMISION NO:</strong> RM-2026-001</td></tr>
            <tr><td style="color: #000000 !important;"><strong>NIT / CÉDULA:</strong> {nit_cliente}</td><td style="text-align:right; color: #000000 !important;"><strong>FECHA EMISIÓN:</strong> {datetime.now().strftime('%d/%m/%Y')}</td></tr>
        </table>
        <table style="width:100%; font-size:14px; border-collapse: collapse; font-family: sans-serif;">
            <thead>
                <tr style="background-color: #1E3A8A; color: white !important; text-align: left;">
                    <th style="padding: 10px; border: 1px solid #CBD5E1; color: white !important;">Descripción del Ítem</th>
                    <th style="padding: 10px; border: 1px solid #CBD5E1; text-align: center; color: white !important;">Cantidad</th>
                    <th style="padding: 10px; border: 1px solid #CBD5E1; text-align: right; color: white !important;">Subtotal Neto</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 12px; border: 1px solid #CBD5E1; color: #000000 !important;">Pasta Alimenticia Funcional Libre de Gluten (Fórmula F1)</td>
                    <td style="padding: 12px; border: 1px solid #CBD5E1; text-align: center; font-weight: bold; color: #000000 !important;">{kilos:,.0f} kg</td>
                    <td style="padding: 12px; border: 1px solid #CBD5E1; text-align: right; color: #000000 !important;">${subtotal_dinero:,.0f}</td>
                </tr>
                <tr style="background-color: #F8FAFC; font-weight: bold;">
                    <td colspan="2" style="padding: 12px; border: 1px solid #CBD5E1; text-align: right; color: #000000 !important;">TOTAL:</td>
                    <td style="padding: 12px; border: 1px solid #CBD5E1; text-align: right; color: #1E3A8A !important; font-size: 16px;">${subtotal_dinero:,.0f} COP</td>
                </tr>
            </tbody>
        </table>
    </div>
    """
    st.markdown(html_remision, unsafe_allow_html=True)
    
    # Estructura de descarga
    df_descarga = pd.DataFrame([{
        "Documento": "Remision Comercial RM-2026-001",
        "Fecha": datetime.now().strftime('%d/%m/%Y'),
        "Cliente": cliente,
        "NIT": nit_cliente,
        "Volumen (KG)": kilos,
        "Total Facturado ($ COP)": subtotal_dinero
    }])
    csv_data = df_descarga.to_csv(index=False).encode('utf-8')
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label="📥 GENERAR Y DESCARGAR REPORTE DIGITAL (EXCEL / CSV)",
        data=csv_data,
        file_name=f"Remision_{cliente.replace(' ', '_')}.csv",
        mime="text/csv"
    )

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
# PESTAÑA 3: PLAN DE PLANTA E INSUMOS CONSOLIDADOS
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
            insumos_totales_kg = [kilos_totales_acumulados * pct for pct in porcentajes.values()]
            costos_totales_insumos = [insumos_totales_kg[i] * list(precios_proveedor.values())[i] for i in range(len(insumos_totales_kg))]
            
            df_consolidado = pd.DataFrame({
                "Materia Prima Requerida": ["Harina de Yuca Industrial", "Harina de Caupí (Frijol)", "Harina de Auyama Deshidratada", "Suministro de Agua Potable", "Huevo Líquido Pasteurizado"],
                "Porcentaje Fórmula": [f"{p*100:.1f}%" for p in porcentajes.values()],
                "Masa Total a Pesar": [f"{k:,.1f} kg" for k in insumos_totales_kg],
                "Presupuesto de Gasto": [f"${c:,.0f} COP" for c in costos_totales_insumos]
            })
            st.dataframe(df_consolidado, width="stretch", hide_index=True)
            
        with col_p2:
            st.markdown("##### 🥧 Distribución de Peso en Tolva")
            fig, ax = plt.subplots(figsize=(4.5, 4.5))
            labels = ['Yuca', 'Caupí', 'Auyama', 'Agua', 'Huevo']
            colors_pie = ["#1E3A8A", "#2563EB", "#F59E0B", "#94A3B8", "#CBD5E1"]
            ax.pie(insumos_totales_kg, labels=labels, autopct='%1.0f%%', startangle=90, colors=colors_pie, textprops={'fontweight':'bold', 'fontsize':10})
            ax.axis('equal')
            plt.tight_layout()
            st.pyplot(fig)

# ------------------------------------------------------------------------------
# PESTAÑA 4: LABORATORIO DE CALIDAD
# ------------------------------------------------------------------------------
with pestana_calidad:
    st.markdown("### 🔬 Módulo de Aseguramiento de Calidad en Línea")
    humedad_ingresada = st.slider("Indique el % de humedad registrado:", min_value=2.0, max_value=10.0, value=4.5, step=0.1)
    if humedad_ingresada <= 5.0:
        st.success(f"🟢 **LOTE APROBADO** | Humedad del {humedad_ingresada:.1f}% cumple con la norma NTC 267.")
    else:
        st.error(f"🔴 **LOTE RECHAZADO** | Humedad del {humedad_ingresada:.1f}% no cumple los parámetros.")

st.markdown("---")
st.caption("🔒 PastaControl Enterprise System • Versión de Alta Fidelidad para Sustentación Pública")
