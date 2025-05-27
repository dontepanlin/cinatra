import os.path as osp

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy

required_conan_version = ">=1.50.0"


class CinatraConan(ConanFile):
    name = "cinatra"
    version = "0.9.5"
    url = "https://github.com/qicosmos/cinatra"
    description = "Cinatra - an efficient and easy-to-use C++ HTTP framework"
    topics = "http", "header-only"
    license = "MIT"
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = "include/*"
    generators = "CMakeToolchain", "CMakeDeps"

    @property
    def _minimum_cpp_standard(self):
        return 20

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, self._minimum_cpp_standard)

    def requirements(self):
        self.requires("asio/1.30.2")

    def package(self):
        copy(self, "LICENSE", dst=osp.join(self.package_folder, "licenses"), src=self.source_folder)
        copy(self, "*", dst=osp.join(self.package_folder, "include"), src=osp.join(self.source_folder, "include"))

    def package_id(self):
        self.info.clear()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "cinatra")
        self.cpp_info.set_property("cmake_target_name", "cinatra::cinatra")
        self.cpp_info.set_property("pkg_config_name", "cinatra")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.frameworkdirs = []
        self.cpp_info.resdirs = []
        self.cpp_info.includedirs = ["include"]
