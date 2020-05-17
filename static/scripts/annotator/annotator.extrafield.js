Annotator.Plugin.ExtraField = function(element) {
  function formatDateTime(d) {
    function _(n) {
      if (n < 10)
        return '0' + n;
      return ''+n;           
    }
    return `${d.getFullYear()}/${_(d.getMonth()+1)}/${_(d.getDate())} ${_(d.getHours())}:${_(d.getMinutes())}:${_(d.getSeconds())}`
    //return '' + d.getFullYear() + '/' + _(d.getMonth() + 1) + '/' + _(d.getDate()) + ' ' + _(d.getHours()) + ':' + _(d.getMinutes()) + ':' + _(d.getSeconds());
  }

  return {
    pluginInit: function() {
      if (!Annotator.supported())
        return;
      this.annotator.viewer.addField({
        load: function(field, annotation) {
          field.style.display = 'flex';
          field.style.justifyContent = 'space-between'
          field.innerHTML = "<span>" + formatDateTime(new Date(annotation.created)) + "</span><span>" + annotation.user + "</span>";
        }
      });
    }
  }
}