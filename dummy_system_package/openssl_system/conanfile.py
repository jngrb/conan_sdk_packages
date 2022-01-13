from conans import CMake, tools, ConanFile
from conans.errors import ConanException
from conans.tools import os_info, SystemPackageTool
import os
import subprocess

class DummyOpenSslConan(ConanFile):
    name = "openssl"
    default_user = "system"
    default_channel = "stable"
    settings = "os"
    exports = "*"
    options = { "shared_openssl": [True, False] }
    default_options = { "shared_openssl": False }

    def set_version(self):
        shcmd="openssl version | cut -d ' ' -f 2"
        self.version = subprocess.check_output(shcmd, shell=True, universal_newlines=True)

    def configure(self):
        if self.settings.os == "Windows":
            raise ConanException("Not supported on Windows")

    def system_requirements(self):
        pack_name = None
        if os_info.linux_distro == "ubuntu":
            pack_name = "libssl-dev"
        elif os_info.linux_distro == "fedora" or os_info.linux_distro == "centos":
            pack_name = "openssl-devel"

        if pack_name:
            installer = SystemPackageTool()
            installer.install(pack_name) # Install the package, will update the package database if pack_name isn't already installed

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "OpenSSL"
        self.cpp_info.names["cmake_find_package_multi"] = "OpenSSL"
        if self.options.shared_openssl:
            self.cpp_info.components["ssl"].libs = ['ssl']
            self.cpp_info.components["crypto"].libs = ['crypto']
        else:
            self.cpp_info.components["ssl"].libs = ['libssl.a']
            self.cpp_info.components["crypto"].libs = ['libcrypto.a']

        self.cpp_info.components["crypto"].system_libs.extend(["dl", "rt"])
        self.cpp_info.components["ssl"].requires = ["crypto"]
        self.cpp_info.components["ssl"].system_libs.append("dl")
        # at least on my Ubuntu 20.04
        self.cpp_info.components["crypto"].system_libs.append("pthread")
        self.cpp_info.components["ssl"].system_libs.append("pthread")

        self.cpp_info.components["crypto"].names["cmake_find_package"] = "Crypto"
        self.cpp_info.components["crypto"].names["cmake_find_package_multi"] = "Crypto"
        self.cpp_info.components["crypto"].names['pkg_config'] = 'libcrypto'
        self.cpp_info.components["ssl"].names["cmake_find_package"] = "SSL"
        self.cpp_info.components["ssl"].names["cmake_find_package_multi"] = "SSL"
        self.cpp_info.components["ssl"].names['pkg_config'] = 'libssl'
