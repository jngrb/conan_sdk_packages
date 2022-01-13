from conans import CMake, tools, ConanFile
from conans.tools import os_info, SystemPackageTool
import os


class OpenSslFromSystemTestConan(ConanFile):
    name = "openssl_from_system_test"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    exports = "*"
    options = { "shared_openssl": [True, False] }
    default_options = { "shared_openssl": False }

    def system_requirements(self):
        pack_name = None
        if os_info.linux_distro == "ubuntu":
            pack_name = "libssl-dev"
        elif os_info.linux_distro == "fedora" or os_info.linux_distro == "centos":
            pack_name = "openssl-devel"

        if pack_name:
            installer = SystemPackageTool()
            installer.install(pack_name) # Install the package, will update the package database if pack_name isn't already installed

    def _build_cmake(self):
        cmake = CMake(self)

        openssl_version = tools.Version("1.1") # how to get openssl version?
        if openssl_version.major == "1" and openssl_version.minor == "1":
            cmake.definitions["OPENSSL_WITH_ZLIB"] = False
        else:
            cmake.definitions["OPENSSL_WITH_ZLIB"] = not self.options["openssl"].no_zlib
        cmake.definitions["OPENSSL_USE_STATIC_LIBS"] = not self.options.shared_openssl
        if self.settings.compiler == 'Visual Studio':
            cmake.definitions["OPENSSL_MSVC_STATIC_RT"] = 'MT' in str(self.settings.compiler.runtime)

        cmake.configure()
        cmake.build()

    def build(self):
        self._build_cmake()

    def package(self):
        self.copy("*digest")

    def test(self):
        if not tools.cross_building(self):
            bin_path = os.path.join("bin", "digest")
            self.run(bin_path, run_environment=True)
        assert os.path.exists(os.path.join(self.deps_cpp_info["openssl"].rootpath, "licenses", "LICENSE"))
