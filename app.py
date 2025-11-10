
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import time

# Importar desde tus archivos
from AStarPathFinder import AStarPathFinder
from grafoscuenca import CUENCA_NODES, GRAPH_EDGES


st.set_page_config(
    page_title="Búsqueda A* - Cuenca",
    page_icon="🗺️",
    layout="wide"
)


st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #4CAF50 0%, #2196F3 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .info-metric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #2196F3;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    .dataframe {
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_pathfinder():
    return AStarPathFinder(CUENCA_NODES, GRAPH_EDGES)

pathfinder = get_pathfinder()


with st.sidebar:
    st.header("⚙️ Configuración de Búsqueda")
    
    st.markdown("### Selecciona el punto de INICIO")
    lugares = sorted(list(CUENCA_NODES.keys()))
    start_point = st.selectbox(
        "Punto de inicio",
        lugares,
        index=lugares.index("Parque Calderón") if "Parque Calderón" in lugares else 0,
        label_visibility="collapsed"
    )
    
    st.markdown("### Selecciona el punto de DESTINO")
    end_point = st.selectbox(
        "Punto de destino",
        lugares,
        index=lugares.index("Puente Roto") if "Puente Roto" in lugares else 1,
        label_visibility="collapsed"
    )
    

    mostrar_nodos = st.checkbox("Mostrar nodos no visitados en el mapa", value=False)

    buscar = st.button("🔍 Buscar Ruta Óptima", type="primary")
   
    if st.button("🗑️ Limpiar"):
        st.rerun()
    

    st.markdown("---")
    st.markdown("### 📚 Guía Práctica")
    st.info("""
    **Asignatura:** Inteligencia Artificial  
    **Tema:** Algoritmos de Búsqueda en Python  
    **Aplicación:** Búsqueda de Rutas Óptimas en Cuenca
    
    **Desarrollado como parte de la práctica académica sobre algoritmos de búsqueda informada.**
    """)


st.markdown("""
<div class="main-header">
    <h1>🗺️ Búsqueda de Rutas Óptimas en Cuenca - Algoritmo A*</h1>
    <p>Esta aplicación implementa el algoritmo de búsqueda A* para encontrar la ruta más corta entre dos puntos de interés en la ciudad de Cuenca, Ecuador. 
    El algoritmo combina la búsqueda informada con una heurística basada en distancia euclidiana para optimizar la exploración del espacio.</p>
</div>
""", unsafe_allow_html=True)


resultado = None


if buscar:
    if start_point == end_point:
        st.error("⚠️ El punto de inicio y destino deben ser diferentes")
    else:
        with st.spinner("🔄 Calculando la ruta óptima..."):
            start_time = time.time()
            path, distance, nodes_explored = pathfinder.find_path(start_point, end_point)
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
        
        resultado = {
            'path': path,
            'distance': distance,
            'nodes_explored': nodes_explored,
            'execution_time': execution_time,
            'explored_list': pathfinder.explored
        }

if resultado and resultado['path']:
    # Mensaje de éxito
    st.markdown(f"""
    <div class="success-box">
        <strong>✅ ¡Ruta encontrada!</strong><br>
        <strong>🛣️ Ruta:</strong> {' → '.join(resultado['path'])}
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-metric">
            <h4>📏 Distancia Total</h4>
            <h2>{:.2f} km</h2>
        </div>
        """.format(resultado['distance']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-metric">
            <h4>🔍 Nodos Explorados</h4>
            <h2>{}</h2>
        </div>
        """.format(resultado['nodes_explored']), unsafe_allow_html=True)
    
 
    st.markdown("### 📋 Detalles de la Ruta")
    
    tabla_datos = []
    for i in range(len(resultado['path'])):
        nodo = resultado['path'][i]
        nodo_data = CUENCA_NODES[nodo]
        
        if i < len(resultado['path']) - 1:
            siguiente = resultado['path'][i + 1]
            dist_segmento = pathfinder.get_distance(nodo, siguiente)
            dist_acumulada = sum(pathfinder.get_distance(resultado['path'][j], resultado['path'][j+1]) 
                                for j in range(i+1))
        else:
            dist_segmento = 0
            dist_acumulada = resultado['distance']
        
        tabla_datos.append({
            'Paso': i + 1,
            'Lugar': nodo,
            'Descripción': nodo_data['descripcion'],
            'Lat': nodo_data['lat'],
            'Lon': nodo_data['lon'],
            'Distancia Segmento (km)': f"{dist_segmento:.3f}",
            'Distancia Acumulada (km)': f"{dist_acumulada:.3f}"
        })
    
    df = pd.DataFrame(tabla_datos)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar detalles (CSV)",
        data=csv,
        file_name=f"ruta_{start_point.replace(' ', '_')}_{end_point.replace(' ', '_')}.csv",
        mime="text/csv"
    )
    

    st.markdown("### 🗺️ Visualización de la Ruta en Mapa")
    
    cuenca_center = [-2.9005, -79.0010]
    mapa = folium.Map(
        location=cuenca_center,
        zoom_start=14,
        tiles="OpenStreetMap"
    )
    
    if mostrar_nodos:
        for nombre, datos in CUENCA_NODES.items():
            if nombre not in resultado['path']:
                folium.CircleMarker(
                    location=[datos["lat"], datos["lon"]],
                    radius=5,
                    popup=nombre,
                    color="gray",
                    fill=True,
                    fillColor="lightgray",
                    fillOpacity=0.5
                ).add_to(mapa)
    
    route_coords = []
    for node in resultado['path']:
        node_data = CUENCA_NODES[node]
        route_coords.append([node_data["lat"], node_data["lon"]])
    
    folium.PolyLine(
        route_coords,
        color="#2196F3",
        weight=6,
        opacity=0.8
    ).add_to(mapa)
    
    for i, node in enumerate(resultado['path']):
        node_data = CUENCA_NODES[node]
        
        if i == 0:
            folium.Marker(
                location=[node_data["lat"], node_data["lon"]],
                popup=f"<b>🟢 INICIO</b><br>{node}",
                tooltip=f"Inicio: {node}",
                icon=folium.Icon(color="green", icon="play", prefix='glyphicon')
            ).add_to(mapa)
        elif i == len(resultado['path']) - 1:
            folium.Marker(
                location=[node_data["lat"], node_data["lon"]],
                popup=f"<b>🔴 DESTINO</b><br>{node}",
                tooltip=f"Destino: {node}",
                icon=folium.Icon(color="red", icon="flag", prefix='glyphicon')
            ).add_to(mapa)
        else:
            folium.CircleMarker(
                location=[node_data["lat"], node_data["lon"]],
                radius=8,
                popup=f"<b>Paso {i+1}</b><br>{node}",
                tooltip=f"Paso {i+1}: {node}",
                color="#2196F3",
                fill=True,
                fillColor="white",
                fillOpacity=1,
                weight=3
            ).add_to(mapa)
    
    st_folium(mapa, width=None, height=500, returned_objects=[])
    
elif resultado and not resultado['path']:
    st.error("❌ No se encontró una ruta entre estos puntos. Verifica que estén conectados en el grafo.")

else:
    st.info("👈 Configura los puntos de inicio y destino en el panel lateral, luego presiona **Buscar Ruta Óptima**")
    
    st.markdown("### 🗺️ Puntos de Interés en Cuenca")
    
    cuenca_center = [-2.9005, -79.0010]
    mapa_inicial = folium.Map(
        location=cuenca_center,
        zoom_start=13,
        tiles="OpenStreetMap"
    )
    
    for nombre, datos in CUENCA_NODES.items():
        color = "green" if nombre == start_point else "red" if nombre == end_point else "blue"
        folium.Marker(
            location=[datos["lat"], datos["lon"]],
            popup=f"<b>{nombre}</b><br>{datos['descripcion']}",
            tooltip=nombre,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(mapa_inicial)
    
    st_folium(mapa_inicial, width=None, height=500, returned_objects=[])


st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><b>Instituto Superior Tecnológico del Azuay</b></p>
    <p>Asignatura: Inteligencia Artificial | Ciclo: M6A | Período: 2025-I</p>
    <p>Docente: Mgtr. Verónica Paulina Chimbo Coronel</p>
</div>
""", unsafe_allow_html=True)