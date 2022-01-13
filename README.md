# How to use certain libraries from the underlying system (SDK)?

## Purpose

## Examples

The example is taken from the openss test package in the [Conan Center Index](https://github.com/conan-io/conan-center-index/tree/master/recipes/openssl/1.x.x/test_package).

### Pure CMAKE

Consume the system library using pure CMake.

```[bash]
sudo apt-get install build_essential make gcc cmake libssl-dev

cd pure_cmake
mkdir build
cd build
cmake ..
make
./digest
```

### Consume from Conan Center Index

Consume the openssl library via conan-center-index using conan and CMake.

```[bash]
sudo apt-get install python3 python3-pip
pip3 install conan==1.43.2

cd conan_center_index
conan create .
```

Consumer cannot override to use the openssl provided by the distribution.

### Consume from System with Conan

Consume the openssl library via conan-center-index using conan and CMake.

```[bash]
cd conan_from_system
export CONAN_SYSREQUIRES_MODE=enabled
conan create .
```

Consumer cannot override to use conan.

### Have a dummy system package

```[bash]
cd dummy_system_package
cd openssl_system
conan create . # on Ubuntu 20.04, this will generate openssl/1.1.1f@system/stable
cd ..
cd digest_lib
conan create .
cd ..
cd conaumer_cci
conan create .
cd ..
cd conaumer_system
conan create . --build=missing # digest_lib should be re-built
```

Conditions:

* same name as the CCI package so that override works

## License

[MIT License](./LICENSE)
