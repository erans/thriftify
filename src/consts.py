DEFAULT_PACKAGE_NAME_TEMPLATE = "%s_%s_bindings_package.zip"

SUPPORTED_LANGUAGES = {
	"as3" : { 
		"name" : "ActionScript 3",
		"parameters" : {
			"bindable" : "Add [bindable] metadata to all the struct classes." 
		}
	},
	"c_glib" : {
		"name" : "C, using GLib"
	},
	"cocoa" : {
		"name" : "Cocoa",
		"parameters" : {
			"log_unexpected" : "Log every time an unexpected field ID or type is encountered."
		}
	},
	"cpp" : {
		"name" : "C++",
		"parameters" : {
			"cob_style" : 'Generate "Continuation OBject"-style classes.',
			"no_client_completion" : 'Omit calls to completion__() in CobClient class.',
			"templates" : 'Generate templatized reader/writer methods.',
			"purse_enums" : 'Generate pure enums instead of wrapper classes.',
			"dense" : 'Generate type specifications for the dense protocol.',
			"include_prefix" : 'Use full include paths in generated files.'
		}
	},
	"csharp" : {
		"name" : "C#",
		"parameters" : {
			"async" : "Adds Async CTP support.",
			"wcf" : "Adds bindings for WCF to generated classes."
		}
	},
	"d" : {
		"name" : "D"
	},
	"delphi" : {
		"name" : "Delphi",
		"parameters" : {
			"ansistr_binary" : "Use AnsiString as binary properties."
		}
	},
	"erl" : {
		"name" : "Erlang"
	},
	"go" : {
		"name" : "Go"
	},
	"hs" : {
		"name" : "Haskell"
	},
	"html" : {
		"name" : "HTML"
	},
	"java" : {
		"name" : "Java",
		"parameters" : {
			"beans" : "Members will be private, and setter methods will return void.",
			"private-members" : "Members will be private, but setter methods will return 'this' like usual.",
			"nocamel" : "Do not use CamelCase field accessors with beans",
			"hahscode" : "Generate quality hashCode methods.",
			"android_legacy" : "Do not use java.io.IOException(throwable) (available for Android 2.3 and above).",
			"java5" : "Generate Java 1.5 compliant code (includes android_legacy flag)."		
		}
	},
	"javame" : {
		"name" : "Java ME"
	},
	"js" : {
		"name" : "Javascript",
		"parameters" : {
			"jquery" : "Generate jQuery compatible code.",
			"node" : "Generate node.js compatible code."
		}
	},
	"ocaml" : {
		"name" : "OCaml"
	},
	"perl" : {
		"name" : "Perl"
	},
	"php" : {
		"name" : "PHP",
		"parameters" : {
			"inlined" : "Generate PHP inlined files",
			"server" : "Generate PHP server stubs",
			"autoload" : "Generate PHP with autoload",
			"oop" : "Generate PHP with object oriented subclasses",
			"rest" : "Generate PHP REST processors",
			"namespace" : "Generate PHP namespaces as defined in PHP >= 5.3"
		}
	},
	"py" : {
		"name" : "Python",
		"parameters" : {
			"new_style" : "Generate new-style classes.",
			"twisted" : "Generate Twisted-friendly RPC services.",
			"utf8strings" : "Encode/decode strings using utf8 in the generated code.",
    		"slots" : "Generate code using slots for instance members.",
    		"dynamic" : "Generate dynamic code, less code generated but slower.",
    		"dynbase=(.*)" : "Derive generated classes from class CLS instead of TBase.",
    		"dynexc=(.*)" : "Derive generated exceptions from CLS instead of TExceptionBase.",
    		"dynimport='(.*)'" : "Add an import line to generated code to find the dynbase class."
		}
	},
	"rb" : {
		"name" : "Ruby",
		"parameters" : {
			"rubygems" : "Add a \"require 'rubygems'\" line to the top of each generated file."		
		}
	},
	"st" : {
		"name" : "Smalltalk"
	},
	"xsd" : {
		"name" : "XML Schema (XSD)"
	}
}
