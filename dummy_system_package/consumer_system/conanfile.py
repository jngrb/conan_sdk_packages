from conans import CMake, tools, ConanFile
import os


class DigestConsumerSystemConan(ConanFile):
    name = "digest_consumer_system"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake", "cmake_find_package"
    exports = "*"

    def requirements(self):
        self.requires("digest_lib/0.1@")
        # the only line that differs from digest_consumer_cci: override for system openssl
        self.requires("openssl/1.1.1f@system/stable", override=True)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
    
    def package(self):
        self.copy("*digest")

    def test(self):
        if not tools.cross_building(self):
            bin_path = os.path.join("bin", "digest")
            self.run(bin_path, run_environment=True)
        assert os.path.exists(os.path.join(self.deps_cpp_info["openssl"].rootpath, "licenses", "LICENSE"))
