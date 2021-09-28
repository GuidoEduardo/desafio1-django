$(document).ready(() => {
    let table = $('#table');

    $.ajax({
        url: '/table/products/',
        success: (data) => {
            let date,
                columns = data['columns'],
                columnsName = data['columnsName'],
                columnsDateName = data['columnsDateName'];

            columnsName.forEach((element, index, array) => {
                table.find('tr').append('<th>' + element + '</th>');
            });
            
            columnsDateName.forEach((element, index, array) => {                      
                table.find('tr').append('<th>' + new Date(element).toLocaleString('default', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' }) + '</th>');
            });

            table.DataTable({
                "processing": true,
                "serverSide": true,
                "ajax": (data, callback, settings) => { 
                    $.get('/table/products/', {
                        limit: data.length,
                        start: data.start,
                        filters: data.search.value,
                        column:  data.columns[data.order[0].column].data,
                        dir: data.order[0].dir
                    }, (response) => {
                            callback({
                                recordsTotal: response.recordsTotal,
                                recordsFiltered: response.recordsTotal,
                                data: response.objects
                            });
                        },
                    );
                },
                "scrollY": true,
                "scrollX": true,
                "columns": columns,
                "columnDefs": [{
                    "defaultContent": "0",
                    "targets": "_all"
                }],
            })
        }
    });
});