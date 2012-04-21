$(document).ready(function() {
  $('#submit-text-form').submit(function(e) {
    var do_zip = $('#download_zip').prop('checked');
    if (do_zip) {
      return true;
    } else {
      show_progress();
      $.post(e.target.action, $(e.target).serialize(), function(data) {
        render_files(data);
      });
      return false;
    }
  });
});

function show_progress() {
  var html = [];
  html.push("I'm a poor Amazon Micro instance and thrift is so hard! Please wait a sec and leme finish...");
  html.push('<div class="progress progress-striped active"><div class="bar" style="width: 100%;"></div></div>');
  $('#result_files').html(html.join(''));
}

//
// Renders the files from the json data object on the page
//
function render_files(data) {
  var html = [];
  for (var i = 0; i < data.files.length; ++i) {
    var file = data.files[i];
    if (file.name == "file.thrift") {
      continue;
    }
    html.push('<h2>');
    html.push(file.name);
    html.push('</h2>');
    html.push("<pre class='brush: ");
    html.push(file.language);
    html.push("'>");
    html.push(file.content);
    html.push("</pre>");
  };
  $('#result_files').html(html.join(''));
  syntax_highlight();
}

function syntax_highlight() {
  SyntaxHighlighter.highlight();
}