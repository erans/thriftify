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
    var file = data.files[i];
    if (file.name == "file.thrift") {
      continue;
    }
    html.push('<h2>');
    html.push(file.name);
    html.push('</h2>');
    html.push("<pre class='brush: ");
    html.push(data.language);
    html.push("'>");
    html.push(file.content);
    html.push("</pre>");
  };
  $('#result_files').html(html.join(''));
  syntax_highlight();
}

// initialize SyntaxHighlighter
function syntax_highlight_path() {
  var args = arguments, result = [];
       
  for(var i = 0; i < args.length; i++) {
    result.push(args[i].replace('@', '/static/js/sh/'));
  }
  return result
};

function syntax_highlight() {
  SyntaxHighlighter.autoloader.apply(null, syntax_highlight_path(
    'applescript            @shBrushAppleScript.js',
    'actionscript3 as3      @shBrushAS3.js',
    'bash shell             @shBrushBash.js',
    'coldfusion cf          @shBrushColdFusion.js',
    'cpp c                  @shBrushCpp.js',
    'c# c-sharp csharp      @shBrushCSharp.js',
    'css                    @shBrushCss.js',
    'delphi pascal          @shBrushDelphi.js',
    'diff patch pas         @shBrushDiff.js',
    'erl erlang             @shBrushErlang.js',
    'groovy                 @shBrushGroovy.js',
    'java                   @shBrushJava.js',
    'jfx javafx             @shBrushJavaFX.js',
    'js jscript javascript  @shBrushJScript.js',
    'perl pl                @shBrushPerl.js',
    'php                    @shBrushPhp.js',
    'text plain             @shBrushPlain.js',
    'py python              @shBrushPython.js',
    'ruby rails ror rb      @shBrushRuby.js',
    'sass scss              @shBrushSass.js',
    'scala                  @shBrushScala.js',
    'sql                    @shBrushSql.js',
    'vb vbnet               @shBrushVb.js',
    'xml xhtml xslt html    @shBrushXml.js',
    'java                   @shBrushJava.js'
  ));
  SyntaxHighlighter.all();
}