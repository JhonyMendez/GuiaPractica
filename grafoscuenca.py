from typing import Dict

CUENCA_NODES: Dict[str, Dict[str, float]] = {
     "Catedral Nueva": {"lat": -2.8975, "lon": -79.005, "descripcion": "Centro histórico de Cuenca"},
    "Parque Calderón": {"lat": -2.89741, "lon": -79.00438, "descripcion": "Corazón de Cuenca"},
    "Puente Roto": {"lat": -2.90423, "lon": -79.00142, "descripcion": "Monumento histórico"},
    "Museo Pumapungo": {"lat": -2.90607, "lon": -78.99681, "descripcion": "Museo de antropología"},
    "Terminal Terrestre": {"lat": -2.89222, "lon": -78.99277, "descripcion": "Terminal de autobuses"},
    "Mirador de Turi": {"lat": -2.92583, "lon": -79.0040, "descripcion": "Mirador con vista panorámica"},
    "Catedral Vieja": {"lat": -2.89745, "lon": -79.00475, "descripcion": "Primera catedral de Cuenca, hoy Museo"},
    "Río Tomebamba": {"lat": -2.90125, "lon": -79.00235, "descripcion": "Río emblemático de la ciudad"},
    "Mercado 10 de Agosto": {"lat": -2.89580, "lon": -79.00820, "descripcion": "Mercado tradicional más grande"},
    "Plaza de las Flores": {"lat": -2.89820, "lon": -79.00520, "descripcion": "Icónica plaza con vendedoras de flores"},
    "Museo del Sombrero": {"lat": -2.90015, "lon": -79.00385, "descripcion": "Historia del Panama Hat de paja toquilla"},
    "El Barranco": {"lat": -2.90280, "lon": -79.00115, "descripcion": "Paseo ribereño con casas coloniales colgantes"},
    "Parque de la Madre": {"lat": -2.89125, "lon": -79.00945, "descripcion": "Parque familiar con laguna"},
    "Ruinas de Todos Santos": {"lat": -2.89320, "lon": -79.00125, "descripcion": "Complejo arqueológico cañari-inca"},
    "Iglesia del Carmen de la Asunción": {"lat": -2.89695, "lon": -79.00580, "descripcion": "Iglesia con cúpulas y mercado de flores"},
    "Prohibido Centro Cultural": {"lat": -2.90180, "lon": -79.00320, "descripcion": "Espacio cultural en antigua fábrica"},
}

GRAPH_EDGES = {
   "Catedral Nueva": ["Parque Calderón", "Puente Roto", "Museo Pumapungo", "Catedral Vieja", "Plaza de las Flores"],
    "Parque Calderón": ["Catedral Nueva", "Terminal Terrestre", "Puente Roto", "Catedral Vieja"],
    "Puente Roto": ["Catedral Nueva", "Parque Calderón", "Museo Pumapungo", "Mirador de Turi", "Río Tomebamba", "El Barranco"],
    "Museo Pumapungo": ["Catedral Nueva", "Puente Roto", "Terminal Terrestre", "Ruinas de Todos Santos"],
    "Terminal Terrestre": ["Parque Calderón", "Museo Pumapungo", "Mirador de Turi", "Parque de la Madre"],
    "Mirador de Turi": ["Puente Roto", "Terminal Terrestre"],
    "Catedral Vieja": ["Catedral Nueva", "Parque Calderón", "Plaza de las Flores"],
    "Río Tomebamba": ["Puente Roto", "El Barranco", "Museo del Sombrero", "Prohibido Centro Cultural"],
    "Mercado 10 de Agosto": ["Parque de la Madre", "Terminal Terrestre", "Plaza de las Flores"],
    "Plaza de las Flores": ["Catedral Nueva", "Catedral Vieja", "Iglesia del Carmen de la Asunción", "Mercado 10 de Agosto"],
    "Museo del Sombrero": ["Río Tomebamba", "El Barranco", "Prohibido Centro Cultural"],
    "El Barranco": ["Puente Roto", "Río Tomebamba", "Museo del Sombrero", "Prohibido Centro Cultural"],
    "Parque de la Madre": ["Terminal Terrestre", "Mercado 10 de Agosto", "Ruinas de Todos Santos"],
    "Ruinas de Todos Santos": ["Museo Pumapungo", "Parque de la Madre"],
    "Iglesia del Carmen de la Asunción": ["Plaza de las Flores", "Catedral Vieja"],
    "Prohibido Centro Cultural": ["Río Tomebamba", "Museo del Sombrero", "El Barranco"],
}