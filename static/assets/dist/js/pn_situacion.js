// pn_situacion.js

// Para inicializar DataTable de forma segura
let dataTableInstance = null;

document.addEventListener('DOMContentLoaded', function() {

    // Grafico
    const filtroForm = document.getElementById('filtroForm');


    /* 
    / * 1) Evento "Obtener Datos" para la tabla RANKING
    */
    if (obtenerDatosBtn) {
        obtenerDatosBtn.addEventListener('click', function() {
            const anio = document.getElementById('anio-select').value;
            const mes  = document.getElementById('mes-select').value;

        fetch(`index_pn_situacion_actual`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
          // Destruir tabla si ya existe
        if (dataTableInstance) {
            dataTableInstance.destroy();
        }

        if (data.red && data.red.length > 0) {
            showDebugPopup(`Datos recibidos: ${data.length} registros`);
            let tableContent = '';
            data.red.forEach((red, index) => {
            const avanceColor = getAvanceColor(data.avance_r[index]);
            tableContent += `
                <tr>
                    <td style="font-size: 14px;">${data.cero_a[index]}</td>
                    <td class="text-center" style="font-size: 14px;">${data.uno_a[index]}</td>
                    <td class="text-center" style="font-size: 14px;">${data.dos_a[index]}</td>
                    <td class="text-center" style="font-size: 14px;">${data.tres_a[index]}</td>
                    <td class="text-center" style="font-size: 14px;">${data.cuatro_a[index]}</td>
                    <td class="text-center" style="font-size: 14px;">${data.cinco_a[index]}</td>
                    <td class="text-center" style="font-size: 14px; color: ${avanceColor}; font-weight: bold;">
                        ${data.avance_r[index]}%
                    </td>
                </tr>
            `;
        });
        datosTable.innerHTML = tableContent;

        // Inicializar DataTables con jQuery
        dataTableInstance = $('#datos-table').DataTable({
            dom: "<'row'<'col-sm-12 col-md-6'f><'col-sm-12 col-md-6'l>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            language: {
                "decimal": "",
                "emptyTable": "No hay información",
                "info": "Mostrando _START_ a _END_ de _TOTAL_",
                "infoEmpty": "Mostrando 0 a 0 de 0",
                "infoFiltered": "(Filtrado de _MAX_ total)",
                "lengthMenu": "Mostrar _MENU_",
                "loadingRecords": "Cargando...",
                "processing": "Procesando...",
                "search": "Buscar:",
                "zeroRecords": "Sin resultados encontrados",
                "paginate": {
                    "first": "Primero",
                    "last": "Último",
                    "next": "Siguiente",
                    "previous": "Anterior"
                }
            },
            pageLength: 20,
            order: [[3, 'desc']],
            columnDefs: [{ targets: '_all', sortable: true }]
        });
        }   else {
            showDebugPopup('No se recibieron datos');
            datosTable.innerHTML = '<tr><td colspan="4">No hay datos disponibles</td></tr>';
        }           })
        .catch(error => {
            console.error('Error al obtener los datos:', error);
            datosTable.innerHTML = '<tr><td colspan="4">Error al cargar los datos</td></tr>';
        });
    });
    }

/* 
/* 2) Evento "Filtrar" para la gráfica
*/
    if (filtroForm) {
        filtroForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch(`index_pn_situacion_actual?` + new URLSearchParams(formData), {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                return;
            }
            // Mapear mes num => nombre
            const meses = {
                1: 'ENE',  2: 'FEB',  3: 'MAR',  4: 'ABR',
                5: 'MAY',  6: 'JUN',  7: 'JUL',  8: 'AGO',
                9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DIC'
            };
            const nombresMeses = data.mes.map(m => meses[m]);

          // Configurar ECharts
        const option = {
            title: { text: 'EVALUACION MENSUAL' },
            tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
            legend: { data: ['Denominador', 'Numerador', 'Avance'] },
            xAxis: [
                {
                    type: 'category',
                    data: nombresMeses,
                    axisPointer: { type: 'shadow' }
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: 'Cantidad',
                    min: 0,
                    axisLabel: { formatter: '{value}' }
                },
                {
                    type: 'value',
                    name: 'Avance (%)',
                    min: 0,
                    max: 100,
                    interval: 20,
                    axisLabel: { formatter: '{value}%' }
                }
            ],
            series: [
                {
                    name: 'Denominador',
                    type: 'bar',
                    data: data.den,
                    label: {
                        show: true, position: 'top', formatter: '{c}', fontSize: 12, fontWeight: 'bold'
                    },
                    itemStyle: { color: '#91cc75' }
                },
                {
                    name: 'Numerador',
                    type: 'bar',
                    data: data.num,
                    label: {
                        show: true, position: 'top', formatter: '{c}', fontSize: 12, fontWeight: 'bold'
                    },
                    itemStyle: { color: '#fac858' }
                },
                {
                    name: 'Avance',
                    type: 'line',
                    yAxisIndex: 1,
                    data: data.avance,
                    itemStyle: { color: '#5470c6' },
                    label: {
                        show: true, position: 'top', formatter: '{c}%', fontSize: 12, fontWeight: 'bold'
                    }
                }
            ]
            };
            myChart.setOption(option);
        })
            .catch(error => {
                console.error('Error al obtener los datos:', error);
        });
        });
        }
    });
