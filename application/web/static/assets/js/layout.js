$('#error-submit-button').on( "click", function() {
    $('#error-modal').modal('hide');
} );


activar_tooltip = function(){
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    })
}

activar_collapse = function(){
    var collapseElementList = [].slice.call(document.querySelectorAll('.collapse'))
    var collapseList = collapseElementList.map(function (collapseEl) {
      return new bootstrap.Collapse(collapseEl)
    })
}

activar_elements = function(){
    activar_tooltip();
    activar_collapse();
}