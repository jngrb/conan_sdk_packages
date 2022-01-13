# How to use certain libraries from the underlying system (SDK)?

## Purpose

## Examples

The example is taken from the openssl test package in the [Conan Center Index](https://github.com/conan-io/conan-center-index/tree/master/recipes/openssl/1.x.x/test_package).

Note that in call cases, linking OpenSSL is done with these two CMake lines:

```[cmake]
find_package(OpenSSL REQUIRED)

target_link_libraries(digest OpenSSL::SSL)
```

### Pure CMAKE

Consume the system library using pure CMake.

* [CMake listing](pure_cmake/CMakeLists.txt)

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

* [Conan recipe](conan_center_index/conanfile.py)
* [CMake listing](conan_center_index/CMakeLists.txt)

```[bash]
sudo apt-get install python3 python3-pip
pip3 install conan==1.43.2

cd conan_center_index
conan create .
```

Consumer cannot override to use the openssl provided by the distribution.

### Consume from System with Conan

Consume the openssl library via conan-center-index using conan and CMake.

* [Conan recipe](conan_from_system/conanfile.py)
* [CMake listing](conan_from_system/CMakeLists.txt)

```[bash]
cd conan_from_system
export CONAN_SYSREQUIRES_MODE=enabled
conan create .
```

Consumer cannot override to use conan.

### Have a dummy system package

Dummy openssl package:

* [Conan recipe](dummy_system_package/openssl_system/conanfile.py)

Intermediate library:

* [Conan recipe](dummy_system_package/digest_lib/conanfile.py)
* [CMake listing](dummy_system_package/digest_lib/CMakeLists.txt)

Consumer prefering conan:

* [Conan recipe](dummy_system_package/consumer_cci/conanfile.py)
* [CMake listing](dummy_system_package/consumer_cci/CMakeLists.txt)

Consumer prefering system:

* [Conan recipe](dummy_system_package/consumer_system/conanfile.py)
* [CMake listing](dummy_system_package/consumer_system/CMakeLists.txt)

```[bash]
cd dummy_system_package
cd openssl_system
conan create . # on Ubuntu 20.04, this will generate openssl/1.1.1f@system/stable
cd ..
cd digest_lib
conan create .
cd ..
cd consumer_cci
conan create .
cd ..
cd consumer_system
conan create . --build=digest_consumer_system --build=digest_lib # digest_lib should be re-built
```

Result:

* The consumer can decide where the OpenSSL library should come from. The difference is a *single line of code*: the requirement override in the consuming conan recipe.
* **No a single adaption in the intermediate library needed!**
* See the digest executable an the respective 'bin' subfolders of the produced packages. Check ldd of these and execute them.

Conditions:

* "system" package should have the same name as the CCI package so that override works
* the (most iumportant) options of the CCI package should be reflected in the dummy package (here: option *shared*)
* In order to have a real rebuild of the intermediate library, the intermediate lib should use the full_package_mode for the openssl lib. Alternatively, the version can be changed so something non-semver (I use "system" as version, not as channel). But then, the version reflection in `openssl_version = tools.Version(self.deps_cpp_info["openssl"].version)` would no longer work. And of course any version ranges specified by the consumer.

## License

[MIT License](./LICENSE)
