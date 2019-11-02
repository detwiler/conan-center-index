from conans.model.conan_file import ConanFile, tools
from conans import CMake
import os
import sys


class DefaultNameConan(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        if self.options["boost"].header_only:
            cmake.definitions["HEADER_ONLY"] = "TRUE"
        else:
            cmake.definitions["Boost_USE_STATIC_LIBS"] = not self.options["boost"].shared
        if not self.options["boost"].without_python:
            cmake.definitions["WITH_PYTHON"] = "TRUE"
            cmake.definitions["PYTHON_VERSION"] = self.deps_user_info["boost"].python_version

        cmake.configure()
        cmake.build()

    def test(self):
        if tools.cross_building(self.settings):
            return
        bt = self.settings.build_type
        self.run('ctest --output-on-error -C %s' % bt, run_environment=True)
        if not self.options["boost"].without_python:
            os.chdir("lib")
            sys.path.append(".")
            import libhello_ext
            libhello_ext.greet()
