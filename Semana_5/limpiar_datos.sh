#!/bin/bash
# Script para limpiar todos los datos generados en la Semana 5

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║          🗑️  LIMPIEZA DE DATOS - SEMANA 5                   ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Función para preguntar confirmación
confirmar() {
    read -p "¿Estás seguro de que quieres eliminar todos los datos? (s/n): " respuesta
    case "$respuesta" in
        [sS]|[sS][iI])
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Pedir confirmación
if ! confirmar; then
    echo "❌ Operación cancelada."
    exit 0
fi

echo ""
echo "🧹 Limpiando datos..."
echo ""

# Contador de archivos eliminados
archivos_eliminados=0

# Limpiar datos del framework/tienda_ejemplo
if [ -d "framework/datos/tienda_ejemplo" ]; then
    echo "   🗑️  Eliminando datos de ejemplo (tienda)..."
    rm -rf framework/datos/tienda_ejemplo
    archivos_eliminados=$((archivos_eliminados + 1))
fi

# Limpiar datos del desafío (todos los subdirectorios excepto los del ejemplo)
if [ -d "datos" ]; then
    echo "   🗑️  Eliminando datos de tu desafío..."
    # Eliminar solo los archivos JSON dentro de datos/
    find datos -name "*.json" -type f -delete
    archivos_eliminados=$((archivos_eliminados + $(find datos -type f -name "*.json" | wc -l)))
fi

# Limpiar posibles datos en framework/datos
if [ -d "framework/datos" ]; then
    echo "   🗑️  Limpiando framework/datos..."
    find framework/datos -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +
fi

echo ""
echo "✅ Limpieza completada."
echo ""
echo "📊 Resumen:"
echo "   • Datos del ejemplo: limpiados"
echo "   • Datos del desafío: limpiados"
echo "   • Framework: intacto ✓"
echo "   • Código fuente: intacto ✓"
echo ""
echo "💡 Tip: Ejecuta los programas nuevamente para generar datos frescos."
echo ""
