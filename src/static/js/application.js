$(document).ready(function() {
  $('#submit-text-form').submit(function(e) {
    var do_zip = $('#download_zip').prop('checked');
    if (do_zip) {
      return true;
    } else {
      $.post(e.target.action, $(e.target).serialize(), function(data) {
        render_files(data);
      });
      return false;
    }
  });
});

//
// Renders the files from the json data object on the page
//
function render_files(data) {
  html = [];
  for (var i = 0; i < data.files.length; ++i) {
    html.push("<textarea>");
    html.push(data.files[i].content);
    html.push("</textarea>");

  };
  $('#result_files').html(html.join(''));
}