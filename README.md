Thriftify
=========

Thrift compiler as a service.    
Help you avoid compiling the whole thrift package just to get thrift bindings for a thrift IDL file.    


Written by Eran Sandler (@erans)    
http://eran.sandler.co.il    
http://forecastcloudy.net (@forecastcloudy)    

Inspired by a set of tweet by @scode and @rantav    
https://twitter.com/rantav/status/189643309172539392    

Installation
------------
- Install tornado (sudo easy_install tornado, or see http://www.tornadoweb.org/)
- Install thrift. YMMV but here's a simple recepie for osx using brew:
  - brew update
  - brew install boost
  - brew install libevent
  - Download thrift from http://thrift.apache.org/download/ and unzip
  - cd thrift-x.x.x
  - ./configure --prefix=/usr/local/ --with-boost=/usr/local/Cellar/boost --with-libevent=/usr/local/Cellar/libevent --disable-static
  - make install
  - validate and run thrift from: /usr/local/bin/thrift
- Copy prod_settings.py to settings.py (or symlink, YMMV).
- Run src/thriftiy.py

