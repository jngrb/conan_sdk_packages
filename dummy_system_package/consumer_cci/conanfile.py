from conans import CMake, tools, ConanFile
import os


class DigestConsumerCciConan(ConanFile):
    name = "digest_consumer_cci"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake", "cmake_find_package"
    exports = "*"

    def requirements(self):
        self.requires("digest_lib/0.1@")

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
