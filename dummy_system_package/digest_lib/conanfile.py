from conans import CMake, tools, ConanFile
import os


class DigestLibConan(ConanFile):
    name = "digest_lib"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake", "cmake_find_package"
    exports = "*"

    def requirements(self):
        self.requires("openssl/1.1.1k@")

    def _build_cmake(self, use_find_package):
        cmake = CMake(self)

        if self.settings.os == "Android":
            cmake.definitions["CONAN_LIBCXX"] = ""
        openssl_version = tools.Version(self.deps_cpp_info["openssl"].version)
        if openssl_version.major == "1" and openssl_version.minor == "1":
            cmake.definitions["OPENSSL_WITH_ZLIB"] = False
        else:
            cmake.definitions["OPENSSL_WITH_ZLIB"] = not self.options["openssl"].no_zlib
        cmake.definitions["USE_FIND_PACKAGE"] = use_find_package
        #cmake.definitions["OPENSSL_ROOT_DIR"] = self.deps_cpp_info["openssl"].rootpath
        cmake.definitions["OPENSSL_USE_STATIC_LIBS"] = not self.options["openssl"].shared
        if self.settings.compiler == 'Visual Studio':
            cmake.definitions["OPENSSL_MSVC_STATIC_RT"] = 'MT' in str(self.settings.compiler.runtime)

        cmake.configure()
        cmake.build()

    def build(self):
        self._build_cmake(use_find_package=True)
        self._build_cmake(use_find_package=False)

    def package(self):
        self.copy("*digest*", src="lib", dst="lib")
        self.copy("digest.h", dst="include")

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "Digest"
        self.cpp_info.names["cmake_find_package_multi"] = "Digest"
        self.cpp_info.include_dir = ['include']
        self.cpp_info.libs = ['digest']
        self.cpp_info.requires = ["openssl::openssl"]
