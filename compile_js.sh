
echo Compiling all Syntax Highlight files into one sh-all.js
rm src/static/js/sh/sh-all.js
#
# jscompile uses google's closure compiler and is aliased as in:
# alias jscompile="java -jar .../compiler.jar"
#
JS_COMPILE='java -jar /Users/ran/dev/obgit/trunk/devtools/bin/closure-js-compiler/compiler.jar'
$JS_COMPILE --js src/static/js/sh/shCore.js\
          --js src/static/js/sh/shBrushCpp.js\
          --js src/static/js/sh/shBrushJava.js\
          --js src/static/js/sh/shBrushRuby.js\
          --js src/static/js/sh/shBrushAS3.js\
          --js src/static/js/sh/shBrushDelphi.js\
          --js src/static/js/sh/shBrushPerl.js\
          --js src/static/js/sh/shBrushScala.js\
          --js src/static/js/sh/shBrushPhp.js\
          --js src/static/js/sh/shBrushErlang.js\
          --js src/static/js/sh/shBrushPlain.js\
          --js src/static/js/sh/shBrushVb.js\
          --js src/static/js/sh/shBrushCSharp.js\
          --js src/static/js/sh/shBrushGroovy.js\
          --js src/static/js/sh/shBrushJScript.js\
          --js src/static/js/sh/shBrushPython.js\
          --js src/static/js/sh/shBrushObjectiveC.js\
          --js src/static/js/sh/shBrushXml.js\
          --js_output_file src/static/js/sh/sh-all.js\
          --compilation_level WHITESPACE_ONLY
ls -alh src/static/js/sh/sh-all.js
